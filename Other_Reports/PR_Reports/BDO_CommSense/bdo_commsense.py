import streamlit as st
import pandas as pd
import openpyxl
from pathlib import Path
from Other_Reports.PR_Reports.BDO_CommSense.bdo_format import sheet_formating, individual_sheet_formatting

def bdo_initial(cleaned_file):

    st.checkbox('All PR Releases', key='all_pr')

    if st.session_state['all_pr'] == False:

        month_option = st.selectbox('PR for what month?',[
                                        'JANUARY',
                                        'FEBRUARY',
                                        'MARCH',
                                        'APRIL',
                                        'MAY',
                                        'JUNE',
                                        'JULY',
                                        'AUGUST',
                                        'SEPTEMBER',
                                        'OCTOBER',
                                        'NOVEMBER',
                                        'DECEMBER'], index=None, placeholder="Select Month", key='option_month')
        
        year_option = st.selectbox('Select a year',[
                                    '2024',
                                    '2025',
                                    '2026'], index=None, placeholder="Select Year", key='option_year')
    else:
        st.session_state['option_month'] = 'all'
        st.session_state['option_year'] = 'all'

    tab5_submit = st.button('Submit')

    # if tab5_submit and st.session_state['client_name5'] == "BDO-Comm&Sense":
    if tab5_submit:
        bdo_main(cleaned_file, st.session_state['option_month'], st.session_state['option_year'])

    return


def excel_to_dataframe(xlsx_file):

    return pd.read_excel(xlsx_file)


def create_pr_summary_sheet(result_file, df, pr_category):

    # create list of categories to remove
    pr_cat = [pr_category]

    # create a new df after removing the categories
    if pr_cat != ['']:
        df_new = df[df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))
    else:
        pr_cat = ['Industry', 'BDO News', 'Competitor News']
        df_new = df[~df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))

    # create summary dataframe
    pr_title_count = []
    online_count = []
    print_count = []
    pr_ad_value = []
    pr_pr_value = []
    pr_total_count = []
    title_count = 0
    for pr_title in pr_titles:

        count_online = 0
        count_print = 0
        ad_value = 0
        pr_value = 0
        for j in df.index:
            if df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] in ['Broadsheet', 'Tabloid', 'Magazine', 'Provincial']:
                count_print += 1
                ad_value += df.at[j, 'Ad Value']
                pr_value += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] in ['Online News', 'Blogs']:
                count_online += 1
                ad_value += df.at[j, 'Ad Value']
                pr_value += df.at[j, 'PR Value']
            else:
                pass
        
        title_count += 1
        pr_title_count.append(title_count)

        total_count = count_online + count_print

        online_count.append(count_online)
        print_count.append(count_print)
        pr_ad_value.append(ad_value)
        pr_pr_value.append(pr_value)
        pr_total_count.append(total_count)

    df_summary = pd.DataFrame()

    df_summary.insert(0,'NUMBER', pr_title_count)
    df_summary.insert(1,'BUSINESS UNIT', None)
    df_summary.insert(2, 'CATEGORY', None)
    df_summary.insert(3, 'TITLE', pr_titles)
    df_summary.insert(4, 'DATE RELEASED', None)
    df_summary.insert(5, 'PRINT PICK-UPS', print_count)
    df_summary.insert(6,'ONLINE PICK-UPS', online_count)
    df_summary.insert(7, 'AD VALUE', pr_ad_value)
    df_summary.insert(8, 'PR VALUE', pr_pr_value)
    df_summary.insert(9, 'TO DATE', pr_total_count)
    df_summary.insert(10, 'AVE TO DATE', pr_ad_value)
    df_summary.insert(11, 'PR TO DATE', pr_pr_value)

    l = df_summary.shape[0]
    df_summary.loc[l+1, 'NUMBER'] = 'TOTAL'
    df_summary.loc[l+1, ['PRINT PICK-UPS', 'ONLINE PICK-UPS', 'AD VALUE', 'PR VALUE', 'TO DATE', 'AVE TO DATE', 'PR TO DATE']] = df_summary[['PRINT PICK-UPS', 'ONLINE PICK-UPS', 'AD VALUE', 'PR VALUE', 'TO DATE', 'AVE TO DATE', 'PR TO DATE']].sum()

    writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    df_summary.to_excel(writer, sheet_name='SUMMARY', index=False, startrow=4)
    writer.close()
    
    return


def individual_pr_sheets(result_file, df, pr_category):

    # create list of categories to remove
    pr_cat = [pr_category]

    # create a new df after removing the categories
    if pr_cat != ['']:
        df_new = df[df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))
    else:
        pr_cat = ['Industry', 'BDO News', 'Competitor News']
        df_new = df[~df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))


    for pr_title in pr_titles:
        # use the title as sheetname
        sheet_name = pr_title[:25]

        # create a new df by filtering the company columun by the pr title
        df_pr = df.groupby('Company').get_group(pr_title).reset_index(drop=True)

        # remove the other columns and retain the following columns
        df_pr = df_pr[['Media Type', 'Title', 'Publication', 'Med Page', 'Date', 'Ad Value', 'PR Value', 'v3 - Link']]

        # insert new columns to the created data frame
        df_pr.insert(8, 'IMAGE ATTACHED', None)
        df_pr.insert(9, 'CIRCULATION / SUBSCRIBERS / FOLLOWERS', None)
        df_pr.insert(10,'VIEWS', None)
        df_pr.insert(11, 'LIKES / REACTIONS', None)
        df_pr.insert(12, 'COMMENTS', None)
        df_pr.insert(13, 'SHARES', None)
        df_pr.insert(14, 'TONE', None)
        df_pr.insert(15, 'PRESS RELEASE PICK-UP', None)
        df_pr.insert(16, 'AGENCY-GENERATED PICK-UP', None)

        # re-arrange the columns
        df_pr = df_pr[['Media Type', 'Title', 'Publication', 'IMAGE ATTACHED', 'Med Page', 'Date', 'Ad Value', 'PR Value', 'v3 - Link', 'CIRCULATION / SUBSCRIBERS / FOLLOWERS', 'VIEWS', 'LIKES / REACTIONS', 'COMMENTS', 'SHARES', 'TONE', 'PRESS RELEASE PICK-UP', 'AGENCY-GENERATED PICK-UP']]
        
        # create a new data frame for media type tally
        df_media = df_pr.value_counts('Media Type').reset_index()
        df_media.rename(columns={'Media Type':'MEDIA TYPE', 'count':'COUNT'}, inplace=True)

        l = df_media.shape[0]
        df_media.loc[l+1, 'MEDIA TYPE'] = 'TOTAL'
        df_media.loc[l+1, ['COUNT']] = df_media[['COUNT']].sum()

        # rename the columns of the data frame
        df_pr.rename(columns={
            'Media Type':'TRADITIONAL / ONLINE / S0CIAL MEDIA',
            'Title':'TITLE',
            'Publication':'PUBLICATION',
            'Med Page':'SECTION / PAGE',
            'Date':'DATE OF PUBLICATION',
            'Ad Value':'AD VALUE',
            'PR Value':'PR VALUE',
            'v3 - Link':'LINK'}, inplace=True)
        
        # place a total at the end of the data frame
        l = df_pr.shape[0]
        df_pr.loc[l+1, 'TRADITIONAL / ONLINE / S0CIAL MEDIA'] = 'TOTAL'

        # place total of the columns below
        df_pr.loc[l+1, ['AD VALUE', 'PR VALUE']] = df_pr[['AD VALUE', 'PR VALUE']].sum()
        

        # st.dataframe(df)
        # st.dataframe(df_media)
        
        writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        df_pr.to_excel(writer, sheet_name=sheet_name, index=False, startrow=4)
        df_media.to_excel(writer, sheet_name=sheet_name, index=False, startrow=l+8)
        writer.close()

        individual_sheet_formatting(result_file, sheet_name, pr_title)

    return


def other_bdo_news_sheet(result_file, df, pr_category):

    # create list of categories to remove
    pr_cat = [pr_category]

    # create list of PR Article IDs
    if pr_cat != ['']:
        df_pr_id = df[df['Category'].isin(pr_cat)]
        pr_ids = df_pr_id['Article ID'].to_list()
        pr_ids = list(dict.fromkeys(pr_ids))
    else:
        pr_cat = ['Industry', 'BDO News', 'Competitor News']
        df_pr_id = df[~df['Category'].isin(pr_cat)]
        pr_ids = df_pr_id['Article ID'].to_list()
        pr_ids = list(dict.fromkeys(pr_ids))

    df_bdo = df.groupby('Company').get_group('Banco de Oro').reset_index(drop=True)
    df_bdo = df_bdo[~df_bdo['Article ID'].isin(pr_ids)]

    # remove the other columns and retain the following columns
    df_bdo = df_bdo[['Media Type', 'Title', 'Publication', 'Med Page', 'Date', 'Ad Value', 'PR Value', 'v3 - Link']]

    # insert new columns to the created data frame
    df_bdo.insert(8, 'IMAGE ATTACHED', None)
    df_bdo.insert(9, 'CIRCULATION / SUBSCRIBERS / FOLLOWERS', None)
    df_bdo.insert(10,'VIEWS', None)
    df_bdo.insert(11, 'LIKES / REACTIONS', None)
    df_bdo.insert(12, 'COMMENTS', None)
    df_bdo.insert(13, 'SHARES', None)
    df_bdo.insert(14, 'TONE', None)
    df_bdo.insert(15, 'PRESS RELEASE PICK-UP', None)
    df_bdo.insert(16, 'AGENCY-GENERATED PICK-UP', None)

    # re-arrange the columns
    df_bdo = df_bdo[['Media Type', 'Title', 'Publication', 'IMAGE ATTACHED', 'Med Page', 'Date', 'Ad Value', 'PR Value', 'v3 - Link', 'CIRCULATION / SUBSCRIBERS / FOLLOWERS', 'VIEWS', 'LIKES / REACTIONS', 'COMMENTS', 'SHARES', 'TONE', 'PRESS RELEASE PICK-UP', 'AGENCY-GENERATED PICK-UP']]
    
    # create a new data frame for media type tally
    df_media = df_bdo.value_counts('Media Type').reset_index()
    df_media.rename(columns={'Media Type':'MEDIA TYPE', 'count':'COUNT'}, inplace=True)

    # rename the columns of the data frame
    df_bdo.rename(columns={
        'Media Type':'TRADITIONAL / ONLINE / S0CIAL MEDIA',
        'Title':'TITLE',
        'Publication':'PUBLICATION',
        'Med Page':'SECTION / PAGE',
        'Date':'DATE OF PUBLICATION',
        'Ad Value':'AD VALUE',
        'PR Value':'PR VALUE',
        'v3 - Link':'LINK'}, inplace=True)
    
    # place a total at the end of the data frame
    l = df_bdo.shape[0]
    df_bdo.loc[l+1, 'TRADITIONAL / ONLINE / S0CIAL MEDIA'] = 'TOTAL'

    # place total of the columns below
    df_bdo.loc[l+1, ['AD VALUE', 'PR VALUE']] = df_bdo[['AD VALUE', 'PR VALUE']].sum()

    writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    df_bdo.to_excel(writer, sheet_name='Other BDO News', index=False, startrow=4)
    df_media.to_excel(writer, sheet_name='Other BDO News', index=False, startrow=l+8)
    writer.close()

    return


def pr_comparative_sheet(result_file, df, pr_category):

    # create list of categories to remove
    pr_cat = [pr_category]

    # create a new df after removing the categories
    if pr_cat != ['']:
        df_new = df[df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))
    else:
        pr_cat = ['Industry', 'BDO News', 'Competitor News']
        df_new = df[~df['Category'].isin(pr_cat)]
        pr_titles = df_new['Company'].to_list()
        pr_titles = list(dict.fromkeys(pr_titles))

    # get the count of pr titles
    pr_title_count = []
    for i in range(len(pr_titles)):
        pr_title_count.append(i+1)


    national_broadsheet = []
    national_broadsheet_value = []
    national_tabloid = []
    national_tabloid_value = []
    regional_publication = []
    regional_publication_value = []
    online_publication = []
    online_publication_value = []
    broadcast = []
    broadcast_value = []
    sub_total = []
    sub_total_value = []

    for pr_title in pr_titles:

        broadsheet_count = 0
        broadsheet_value = 0
        tabloid_count = 0
        tabloid_value = 0
        provincial_count = 0
        provincial_value = 0
        web_count = 0
        web_value = 0
        broadcast_count = 0
        broadcast_val = 0

        for j in df.index:
            if df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] == 'Broadsheet':
                broadsheet_count += 1
                broadsheet_value += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] == 'Tabloid':
                tabloid_count += 1
                tabloid_value += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] == 'Provincial':
                provincial_count += 1
                provincial_value += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] in ['Online News', 'Blogs']:
                web_count += 1
                web_value += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == pr_title and df.at[j, 'Media Type'] in ['Radio', 'TV']:
                broadcast_count += 1
                broadcast_val += df.at[j, 'PR Value']

            my_sub_total = broadsheet_count + tabloid_count + provincial_count + web_count + broadcast_count
            my_sub_total_value = broadsheet_value + tabloid_value + provincial_value + web_value + broadcast_val

        national_broadsheet.append(broadsheet_count)
        national_broadsheet_value.append(broadsheet_value)
        national_tabloid.append(tabloid_count)
        national_tabloid_value.append(tabloid_value)
        regional_publication.append(provincial_count)
        regional_publication_value.append(provincial_value)
        online_publication.append(web_count)
        online_publication_value.append(web_value)
        broadcast.append(broadcast_count)
        broadcast_value.append(broadcast_val)
        sub_total.append(my_sub_total)
        sub_total_value.append(my_sub_total_value)
    
    # create count data frame    
    df_comparative = pd.DataFrame()
    df_comparative.insert(0,'PR No.', pr_title_count)
    df_comparative.insert(1,'PR Title', pr_titles)
    df_comparative.insert(2, 'National Broadsheet', national_broadsheet)
    df_comparative.insert(3, 'National Tabloid', national_tabloid)
    df_comparative.insert(4, 'Regional Publication', regional_publication)
    df_comparative.insert(5, 'Online Publication', online_publication)
    df_comparative.insert(6,'Broadcast', broadcast)
    df_comparative.insert(7, 'Subtotal', sub_total)

    l = df_comparative.shape[0]

    # create values data frame
    df_comparative_value = pd.DataFrame()
    df_comparative_value.insert(0,'PR No.', pr_title_count)
    df_comparative_value.insert(1,'PR Title', pr_titles)
    df_comparative_value.insert(2, 'National Broadsheet', national_broadsheet_value)
    df_comparative_value.insert(3, 'National Tabloid', national_tabloid_value)
    df_comparative_value.insert(4, 'Regional Publication', regional_publication_value)
    df_comparative_value.insert(5, 'Online Publication', online_publication_value)
    df_comparative_value.insert(6,'Broadcast', broadcast_value)
    df_comparative_value.insert(7, 'Subtotal', sub_total_value)

    writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    df_comparative.to_excel(writer, sheet_name='PR_Comparative', index=False, startrow=0)
    df_comparative_value.to_excel(writer, sheet_name='PR_Comparative', index=False, startrow=l+5)
    writer.close()

    return


def competitor_sheet(result_file, df):

    # create list of categories to remove
    pr_cat = ['Competitor News']

    # create list of BDO competitors
    df_new = df[df['Category'].isin(pr_cat)]
    competitor_list = df_new['Company'].to_list()
    competitor_list = list(dict.fromkeys(competitor_list))

    blog_count_list = []
    blog_prvalue_list = []
    broadsheet_count_list = []
    broadsheet_prvalue_list = []
    magazine_count_list = []
    magazine_prvalue_list = []
    online_count_list = []
    online_prvalue_list = []
    provincial_count_list = []
    provincial_prvalue_list = []
    radio_count_list = []
    radio_prvalue_list = []
    tabloid_count_list = []
    tabloid_prvalue_list = []
    tv_count_list = []
    tv_prvalue_list = []
    total_count_list = []
    total_prvalue_list = []
    
    for competitor in competitor_list:

        blog_count = 0
        blog_prvalue = 0
        broadsheet_count = 0
        broadsheet_prvalue = 0
        magazine_count = 0
        magazine_prvalue = 0
        online_count = 0
        online_prvalue = 0
        provincial_count = 0
        provincial_prvalue = 0
        radio_count = 0
        radio_prvalue = 0
        tabloid_count = 0
        tabloid_prvalue = 0
        tv_count = 0
        tv_prvalue = 0
        total_count = 0
        total_prvalue = 0

        for j in df.index:
            if df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Blogs':
                blog_count += 1
                blog_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Broadsheet':
                broadsheet_count += 1
                broadsheet_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Magazine':
                magazine_count += 1
                magazine_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Online News':
                online_count += 1
                online_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Provincial':
                provincial_count += 1
                provincial_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Radio':
                radio_count += 1
                radio_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'Tabloid':
                tabloid_count += 1
                tabloid_prvalue += df.at[j, 'PR Value']
            elif df.at[j, 'Company'] == competitor and df.at[j, 'Media Type'] == 'TV':
                tv_count += 1
                tv_prvalue += df.at[j, 'PR Value']
            else:
                continue
        
            total_count = blog_count + broadsheet_count + magazine_count + online_count + provincial_count + radio_count + tabloid_count + tv_count

            total_prvalue = blog_prvalue + broadsheet_prvalue + magazine_prvalue + online_prvalue + provincial_prvalue + radio_prvalue + tabloid_prvalue + tv_count

        blog_count_list.append(blog_count)
        blog_prvalue_list.append(blog_prvalue)
        broadsheet_count_list.append(broadsheet_count)
        broadsheet_prvalue_list.append(broadsheet_prvalue)
        magazine_count_list.append(magazine_count)
        magazine_prvalue_list.append(magazine_prvalue)
        online_count_list.append(online_count)
        online_prvalue_list.append(online_prvalue)
        provincial_count_list.append(provincial_count)
        provincial_prvalue_list.append(provincial_prvalue)
        radio_count_list.append(radio_count)
        radio_prvalue_list.append(radio_prvalue)
        tabloid_count_list.append(tabloid_count)
        tabloid_prvalue_list.append(tabloid_prvalue)
        tv_count_list.append(tv_count)
        tv_prvalue_list.append(tv_prvalue)
        total_count_list.append(total_count)
        total_prvalue_list.append(total_prvalue)

    dfcompetitor = pd.DataFrame()
    dfcompetitor.insert(0,'Company', competitor_list)
    dfcompetitor.insert(1,'Blog PR Value', blog_prvalue_list)
    dfcompetitor.insert(2,'Blog Count', blog_count_list)
    dfcompetitor.insert(3,'Broadsheet PR Value', broadsheet_prvalue_list)
    dfcompetitor.insert(4,'Broadsheet Count', broadsheet_count_list)
    dfcompetitor.insert(5,'Magazine PR Value', magazine_prvalue_list)
    dfcompetitor.insert(6,'Magazine Count', magazine_count_list)
    dfcompetitor.insert(7,'Online News PR Value', online_prvalue_list)
    dfcompetitor.insert(8,'Online News Count', online_count_list)
    dfcompetitor.insert(9,'Provincial PR Value', provincial_prvalue_list)
    dfcompetitor.insert(10,'Provincial Count', provincial_count_list)
    dfcompetitor.insert(11,'Radio PR Value', radio_prvalue_list)
    dfcompetitor.insert(12,'Radio Count', radio_count_list)
    dfcompetitor.insert(13,'Tabloid PR Value', tabloid_prvalue_list)
    dfcompetitor.insert(14,'Tabloid Count', tabloid_count_list)
    dfcompetitor.insert(15,'TV PR Value', tv_prvalue_list)
    dfcompetitor.insert(16,'TV Count', tv_count_list)
    dfcompetitor.insert(17,'PR Value', total_prvalue_list)
    dfcompetitor.insert(18,'Count', total_count_list)

    # create tally at the end of the data frame
    l = dfcompetitor.shape[0]
    dfcompetitor.loc[l+1, 'Company'] = 'Total'

    dfcompetitor.loc[l+1, ['Blog PR Value', 'Blog Count', 'Broadsheet PR Value', 'Broadsheet Count', 'Magazine PR Value', 'Magazine Count', 'Online News PR Value', 'Online News Count', 'Provincial PR Value', 'Provincial Count', 'Radio PR Value', 'Radio Count', 'Tabloid PR Value', 'Tabloid Count', 'TV PR Value', 'TV Count', 'PR Value', 'Count']] = dfcompetitor[['Blog PR Value', 'Blog Count', 'Broadsheet PR Value', 'Broadsheet Count', 'Magazine PR Value', 'Magazine Count', 'Online News PR Value', 'Online News Count', 'Provincial PR Value', 'Provincial Count', 'Radio PR Value', 'Radio Count', 'Tabloid PR Value', 'Tabloid Count', 'TV PR Value', 'TV Count', 'PR Value', 'Count']].sum()

    writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
    dfcompetitor.to_excel(writer, sheet_name='Comnpetitor News', index=False, startrow=0)
    writer.close()

    return


def bdo_main(xlsx_file, month_option, year_option):

    # create a excelfile
    result_file = Path(__file__).parent/f'BDO_Files/BDO_COMMSENSE.xlsx'
    wb = openpyxl.Workbook(result_file)
    wb.save(result_file)
    wb.close()

    df_main = excel_to_dataframe(xlsx_file)

    if month_option == 'all' and year_option == 'all':
        pr_category = ''
    else:
        pr_category = month_option + ' ' + year_option

    # create a summary sheet
    create_pr_summary_sheet(result_file, df_main, pr_category)

    # create individual sheets for each pr release
    individual_pr_sheets(result_file, df_main, pr_category)

    # create other bdo news sheet
    try:
        other_bdo_news_sheet(result_file, df_main, pr_category)
    except:
        pass
    
    # create comnparative sheet
    pr_comparative_sheet(result_file, df_main, pr_category)

    # create competitor sheet
    competitor_sheet(result_file, df_main)



    wb = openpyxl.load_workbook(result_file)
    del wb['Sheet']
    wb.save(result_file)

    sheet_formating(result_file)

    _file = open(result_file, 'rb')
    st.success(f':red[NOTE:] Downloaded file will go to the :red[Downloads Folder]')
    st.download_button(label='📥 Download Excel File', data= _file, file_name= 'BDO-Comm&Sense PR Report.xlsx')
    return