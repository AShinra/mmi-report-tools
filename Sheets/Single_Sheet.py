import pandas as pd
from Tools import hyperlink_title, add_header, format_tableheaders, add_totals


# generate single listing
def single_sheet_report(dataframe, category, type, fname, report_month, report_year, REPORT_FILE):
    '''
    dataframe:= dataframe name
    category:= category list
    type:= main or comp or ind 
    '''

    if type in ['main', 'comp']:
        if type == 'main':
            h1_header = 'Company News'
        else:
            h1_header = 'Competitor News'

        pvt = dataframe.query('Category==@category').pivot_table(index=['Company', 'Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'v3 - Link', 'Section', 'Length', 'Ad Value', 'PR Value'], aggfunc={'Article ID':'count'}).reset_index()

        pvt.rename(columns={'Article ID':'Count'}, inplace=True)

        # set data types of columns
        pvt['Count'] = pvt['Count'].astype(int)

        # addding sub and grand total
        pvt = add_totals(dataframe=pvt)
        

    elif type == 'ind':
        h1_header = 'Industry News'
        pvt = dataframe.query('Category==@category').pivot_table(index=['Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'v3 - Link', 'Section', 'Length', 'Ad Value', 'PR Value'], aggfunc={'Article ID':'count'}).reset_index()
        
        pvt.rename(columns={'Article ID':'Count'}, inplace=True)

        # set data types of columns
        pvt['Count'] = pvt['Count'].astype(int)
        pvt['Date'] = pvt['Date'].astype('datetime64[ns]')

        l = pvt.shape[0]
        
        pvt.loc[l+1, 'Date'] = f'Grand Total'
        pvt.loc[l+1, ['Ad Value', 'PR Value', 'Count']] = pvt[['Ad Value', 'PR Value', 'Count']].sum()
        pvt = pvt.fillna('')

    # convert pivot file to excel
    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a')
    pvt.to_excel(writer, sheet_name=h1_header, index=False, startrow=6)
    writer.close()

    hyperlink_title(REPORT_FILE, h1_header)
    add_header(REPORT_FILE, h1_header, fname, report_month, report_year)
    format_tableheaders(REPORT_FILE, h1_header)

    return