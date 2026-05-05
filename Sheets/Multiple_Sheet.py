import pandas as pd
from Tools import hyperlink_title, add_header, format_tableheaders



def multiple_sheet_report(dataframe, category, company_list, fname, report_month, report_year, REPORT_FILE):
    '''
    datafarme:= name of dataframe to process
    category:= category list
    company_list:= company listing
    '''

    for _company in company_list:
        pvt = dataframe.query('Category==@category and Company==@_company').pivot_table(index=['Company', 'Date', 'Media Type', 'Article Class', 'Publication', 'Title', 'v3 - Link', 'Section', 'Length', 'Ad Value', 'PR Value'], aggfunc={'Article ID':'count'}).reset_index()
        
        if pvt.empty:
            continue
        else:

            pvt.rename(columns={'Article ID':'Count'}, inplace=True)

            l = pvt.shape[0]

            pvt.loc[l+1, 'Company'] = f'{_company} Total'
            pvt.loc[l+1, 'Count'] = pvt['Count'].sum()

            _comp = _company.title()

            if len(_company) > 30:
                _company = _company[:30]
            else:
                pass

            # convert pivot file to excel
            writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a')
            pvt.to_excel(writer, sheet_name=_company, index=False, startrow=6)
            writer.close()

            hyperlink_title(REPORT_FILE, _company)
            add_header(REPORT_FILE, _company, fname, report_month, report_year)
            format_tableheaders(REPORT_FILE, _company)

    return