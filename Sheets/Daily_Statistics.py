import pandas as pd
from Charts.charts import bar_chart
from Tools import format_datatables
import streamlit as st


def daily_stats(dataframe, category, REPORT_FILE, sht_name):

    table_locations = []
    table_dimensions = []

    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay')

    pvt_count = dataframe.query('Category==@category').pivot_table(index=['Date'], columns=['Media Type'], values=['PR Value'], aggfunc=['count']).fillna(0)
    pvt_count.columns = pvt_count.columns.droplevel(0)
    pvt_count.columns = pvt_count.columns.droplevel(0)
    pvt_count.index= pvt_count.index.strftime('%b-%d-%Y')

    # location of 1st table [row, column]
    table1_loc = [0,16]
    # dimensions of 1st table
    table1_dimension = pvt_count.shape

    table_locations.append(table1_loc)
    table_dimensions.append(table1_dimension)

    pvt_count.to_excel(writer, sheet_name=sht_name, startrow=table1_loc[0], startcol=table1_loc[1])

    pvt_sum = dataframe.query('Category==@category').pivot_table(index=['Date'], columns=['Media Type'], values=['PR Value'], aggfunc=['sum']).fillna(0)
    pvt_sum.columns = pvt_sum.columns.droplevel(0)
    pvt_sum.columns = pvt_sum.columns.droplevel(0)
    pvt_sum.index = pvt_sum.index.strftime('%b-%d-%Y')

    # location of 2nd table [row, column]
    table2_loc = [34,16]
    # dimensions of 2nd table
    table2_dimension = pvt_sum.shape

    table_locations.append(table2_loc)
    table_dimensions.append(table2_dimension)

    pvt_sum.to_excel(writer, sheet_name=sht_name, startrow=table2_loc[0], startcol=table2_loc[1])
    writer.close()

    for i in range(len(table_locations)):

        table_location = table_locations[i]
        table_dimension = table_dimensions[i]

        format_datatables(FILE=REPORT_FILE, SHEET=sht_name, TABLE_LOCATION=table_location, TABLE_SIZE=table_dimension)

    

    return table1_loc, table1_dimension, table2_loc, table2_dimension