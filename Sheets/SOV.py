import pandas as pd
from Charts.charts import bar_chart, pie_chart
from Tools import format_datatables
import streamlit as st


def my_sov(dataframe, category, REPORT_FILE, report_month, report_year, fname):

    table_locations = []
    chart_locations = []
    table_sizes = []
    sheet_name = 'Share of Voice'
    media_type = []

    # set initial row location
    _row = 0
    
    pvt_count = dataframe.query('Category==@category').pivot_table(index=['Date'], columns=['Company'], values=['PR Value'], aggfunc=['count']).fillna(0)
    pvt_count.columns = pvt_count.columns.droplevel(0)
    pvt_count.columns = pvt_count.columns.droplevel(0)
    pvt_count.index= pvt_count.index.strftime('%b-%d-%Y')

    table_locations.append([_row,13])
    chart_locations.append(f'A{_row+1}')
    table_sizes.append(pvt_count.shape)
    media_type.append('Count')

    # new row location
    l, w = pvt_count.shape

    if l < 24:
        l = 24

    _row = l + 3

    pvt_sum = dataframe.query('Category==@category').pivot_table(index=['Date'], columns=['Company'], values=['PR Value'], aggfunc=['sum']).fillna(0)
    pvt_sum.columns = pvt_sum.columns.droplevel(0)
    pvt_sum.columns = pvt_sum.columns.droplevel(0)
    pvt_sum.index = pvt_sum.index.strftime('%b-%d-%Y')

    table_locations.append([_row,13])
    chart_locations.append(f'A{_row+1}')
    table_sizes.append(pvt_sum.shape)
    media_type.append('Value')


    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    pvt_count.to_excel(writer, sheet_name=sheet_name, startrow=table_locations[0][0], startcol=table_locations[0][1])
    pvt_sum.to_excel(writer, sheet_name=sheet_name, startrow=table_locations[1][0], startcol=table_locations[1][1])
    writer.close()

    chart_size = [12.5, 20.5]
    chart_name = 'Share of Voice'

    for i in range(len(table_locations)):
        table_location = table_locations[i]
        table_size = table_sizes[i]
        bar_chart(REPORT_FILE, sheet_name, table_size, table_location, chart_locations[i], chart_size, chart_name, report_month, report_year, fname, media_type[i])
        format_datatables(FILE=REPORT_FILE, SHEET=sheet_name, TABLE_LOCATION=table_location, TABLE_SIZE=table_size)

    # new row location
    l, w = pvt_sum.shape

    if l < 24:
        l = 24

    _row += l + 3

    # create pie charts
    pie_count = dataframe.query('Category==@category').pivot_table(index=['Company'], values=['PR Value'], aggfunc=['sum']).fillna(0)
    pie_sum = dataframe.query('Category==@category').pivot_table(index=['Company'], values=['Ad Value'], aggfunc=['count']).fillna(0)
    data_list = [pie_count, pie_sum]
    pie_data = pd.concat(data_list, axis=1)
    pie_data.columns = pie_data.columns.droplevel(0)
    pie_data = pie_data.rename(columns={'PR Value':'Value', 'Ad Value':'Count'})
    pie_data = pie_data.sort_values(by=['Value'], ascending=False)

    # st.dataframe(pie_data)

    table_location = [_row,8]
    table_dimension = pie_data.shape
    chart_locations = [f'A{_row+1}', f'M{_row+1}']
    chart_size = [12.5, 12.5]
    _type = ['Value', 'Count']

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    pie_data.to_excel(writer, sheet_name=sheet_name, startrow=table_location[0], startcol=table_location[1])
    writer.close()

    for i in range(len(table_location)):
        _data = [table_location[0]+1, table_location[1]+i+2, table_location[0]+table_dimension[0]+1, table_location[1]+i+2]
        _labels = [table_location[0]+2, table_location[1]+1, table_location[0]+table_dimension[0]+1, table_location[1]+1]
        pie_chart(REPORT_FILE, sheet_name, _data, _labels, chart_locations[i], chart_size, chart_name, report_month, report_year, fname, _type[i])

    format_datatables(FILE=REPORT_FILE, SHEET=sheet_name, TABLE_LOCATION=table_location, TABLE_SIZE=table_dimension)

    return