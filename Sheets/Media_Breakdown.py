import pandas as pd
import streamlit as st
from Charts.charts import pie_chart
from openpyxl import load_workbook
from Tools import format_datatables




def media_stats(dataframe, category, REPORT_FILE, sht_name, report_month, report_year, fname):

    # table locations
    table_locations = []

    # table sizes
    table_sizes = []

    # media types for count
    media_types = []
    
    chart_name = 'Media Statistics'
    chart_size = [12,15]

    # initialize writer
    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay')

    # create pivot table
    pvt_count = dataframe.query('Category==@category').pivot_table(index=['Media Type'], aggfunc={'Ad Value':'count', 'PR Value':'sum'}).fillna(0)

    # rename column
    pvt_count.rename(columns={'Ad Value':'Count', 'PR Value':'Value'}, inplace=True)
    
    # sort table
    pvt_count = pvt_count.sort_values(by=['Value'], ascending=False)[:20]
    
    # location of 1st table [row, column]
    table_locations.append([0,10])
    
    # dimensions of 1st table
    table_sizes.append(pvt_count.shape)

    media_types.append('Count')
   
    # save pivot to excel
    pvt_count.to_excel(writer, sheet_name=sht_name, startrow=table_locations[0][0], startcol=table_locations[0][1])

    # get the media l ist
    media_list = pvt_count.index.values.tolist()

    r = 0
    c = 10
    for media in media_list:
        r += 25
        media_types.append(media)
        table_locations.append([r,c])
        pvt = dataframe.query('`Media Type`==@media and Category==@category').pivot_table(index=['Publication'], aggfunc={'Ad Value':'count','PR Value':'sum'}).fillna(0)
        pvt.rename(columns={'Ad Value':'Count','PR Value':'Value'}, inplace=True)

        if media in ['Online News', 'Blogs']:
            pvt.index.names = ['Website']
        elif media in ['TV']:
            pvt.index.names = ['Channel']
        elif media in ['Radio']:
            pvt.index.names = ['Station']

        pvt = pvt.sort_values(by=['Value'], ascending=False)[:20]

        table_sizes.append(pvt.shape)

        pvt.to_excel(writer, sheet_name=sht_name, startrow=r, startcol=c)

    # close writer
    writer.close()

    # create pie charts
    for i in range(len(table_locations)):
        
        table_dimension = table_sizes[i]
        table_location = table_locations[i]
        j = table_locations[i][0]+1
        cht_loc = f'A{j}'
        _type = 'Count'

        _data = [table_location[0]+1, table_location[1]+table_dimension[1], table_location[0]+table_dimension[0]+1, table_location[1]+table_dimension[1]]
        _labels = [table_location[0]+2, table_location[1]+1, table_location[0]+table_dimension[0]+1, table_location[1]+1]

        pie_chart(REPORT_FILE, sht_name, _data, _labels, cht_loc, chart_size, chart_name, report_month, report_year, fname, _type)

        format_datatables(FILE=REPORT_FILE, SHEET=sht_name, TABLE_LOCATION=table_location, TABLE_SIZE=table_dimension)

    for i in range(len(table_locations)):
        
        table_dimension = table_sizes[i]
        table_location = table_locations[i]
        j = table_locations[i][0]+1
        cht_loc = f'O{j}'
        _type = 'Value'

        _data = [table_location[0]+1, table_location[1]+table_dimension[1]+1, table_location[0]+table_dimension[0]+1, table_location[1]+table_dimension[1]+1]
        _labels = [table_location[0]+2, table_location[1]+1, table_location[0]+table_dimension[0]+1, table_location[1]+1]

        pie_chart(REPORT_FILE, sht_name, _data, _labels, cht_loc, chart_size, chart_name, report_month, report_year, fname, _type)
    

    return