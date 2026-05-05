import streamlit as st
import pandas as pd
import json
from streamlit_option_menu import option_menu
import openpyxl
from pathlib import Path
from Tools import del_sheet1
from tools_cleaner import title_cleaner, remove_publications, consistent_pub
import re
from Common import read_excel_file

from summarizer import summarize_text
from favorability import favorability
from roi import roi_col
from tonality import tonality
from readership_circulation import readership_and_circulation
from online_reach import monthly_reach
from publication_edition import publication_edition
from publication_tier import publication_tier


@st.cache_resource
def my_markups():

    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(2) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(4) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)  

    return








# removed publications from list
def rename_columns(df, _data):

    for _old, _new in _data.items():
        if _old == _new:
            continue
        else:
            df = df.rename(columns={_old:_new})
    
    st.success('Renamed Columns')

    return df


# extract data from json file
def extract_from_json(json_file):

    _f = open(f'support_files/{json_file}')

    _data = json.load(_f)
    _f.close()

    return _data


@st.cache_data
def json_data():
    headers = extract_from_json('headers.json')
    pubs = extract_from_json('publications.json')
    rem_pubs = extract_from_json('publications_remove.json')
    tiers = extract_from_json('tier1.json')
    edition = extract_from_json('edition.json')
    reach_print = extract_from_json('reach_print.json')
    reach_online = extract_from_json('reach_online.json')
    return headers, pubs, rem_pubs, tiers, edition, reach_print, reach_online


# main process
def root_process(raw_file, rem_dup, rem_pub, pub_tier, pub_edition, rrc, roi, content_tone, fav, content_sum, fname, name):
    
    # st_time = time.time()

    REPORT_FILE = Path(__file__).parent/f'Temp_Files/Cleaned_{name}.xlsx'
    wb = openpyxl.Workbook(REPORT_FILE)
    wb.save(REPORT_FILE)
    wb.close()

    # convert xlsx to dataframe
    df = read_excel_file(raw_file)
  
    # rename dataframe headers
    df = rename_columns(df, json_data()[0])

    # remove duplicates from dataframe
    if rem_dup:
        orig_length = df.shape[0]
        df.drop_duplicates(inplace=True)
        new_length = df.shape[0]
        removed_rows = orig_length-new_length
        st.success(f'Removed {removed_rows} duplicates')

    # df['Raw Date'] = pd.to_datetime(df['Raw Date'])
    df['Med Page'] = df['Med Page'].astype(str)
    df['Title'] = df['Title'].astype(str)       

    # fix media type column
    df['Media Type'] = df['Media Type'].str.replace('AM Radio', 'Radio')
    df['Media Type'] = df['Media Type'].str.replace('FM Radio', 'Radio')
    
    # clean title, page and author columns
    for i in df.index:
        myPage = df.at[i, 'Med Page']
        myAuthor = df.at[i, 'Author']
        myTitle = df.at[i, "Title"]
                
        df.at[i, 'Title'] = title_cleaner(df['Title'][i], df['Publication'][i])
                
        if myPage in ['0', 0, None, 'nan', '']:
            df.at[i, 'Med Page'] = 'No Page Number'
        else:
            df.at[i, 'Med Page'] = 'Page ' + df.at[i, 'Med Page']
    
        if myAuthor in  ['N A', 'N/A', None, 'nan', '']:
            df.at[i, 'Author'] = 'No Author'      
        
    # make publication names consistent
    df = consistent_pub(df, json_data()[1])

    # remove publications from list
    if rem_pub:
        df = remove_publications(df, json_data()[2])
    
    # add publication tier column
    if pub_tier:
        df = publication_tier(df, json_data()[3])
    
    # add publication edition column
    if pub_edition:
        df = publication_edition(df, json_data()[4])
    
    # add readership, circulation and reach
    if rrc:
        df = readership_and_circulation(df, json_data()[5])
        df = monthly_reach(df, json_data()[6])

    # add roi columns
    if roi:
        df = roi_col(df)
    
    # add content tone
    if content_tone:
        df = tonality(df)
        if fav:
            df = favorability(df)
    
    # add summary
    if content_sum:

        df['Summary'] = ''

        for i in df.index:
            _text = df.loc[i, 'Content']

            if _text in ['', None]:
                _text = df.loc[i, 'Title']
                df.loc[i, 'Summary'] = _text
            else:
                df.loc[i, 'Summary'] = summarize_text(_text)        


    # convert pivot file to excel
    writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a')
    df.to_excel(writer, sheet_name='CLEANED', index=False)
    writer.close()

    # add hyperlink to title column
    # REPORT_FILE = hyperlinked_title_raw(file=REPORT_FILE)

    # delete 1st sheet with no data
    REPORT_FILE = del_sheet1(REPORT_FILE)

    result_file = open(REPORT_FILE, 'rb')
    st.success(f':red[NOTE:] Downloaded file will go to the :red[Downloads Folder]')
    st.download_button(label='📥 Download Cleaned Raw', data=result_file ,file_name= f'{fname}.xlsx')

    return


def checkbox_select(raw_file, fname, name):

    # get the file zie
    # bytes_data = raw_file.getvalue()
    # file_size = len(bytes_data)

    # if file_size > 40000000:
    #     st.warning(':blue[File is above 40Mb. Tonality is disabled. Process resulting file in separate tonality function]')

    st.checkbox('Select all', value=False, label_visibility="visible", key='select_all')

    if st.session_state['select_all']:
        st.session_state['rem_dup'] = True
        st.session_state['rem_pub'] = True
        st.session_state['pub_tier'] = True
        st.session_state['pub_edition'] = True
        st.session_state['rrc'] = True
        st.session_state['roi'] = True
        st.session_state['content_tone'] = True
        st.session_state['fav'] = True
        st.session_state['summary_content'] = True

    checks = st.columns(3)

    # if file_size > 40000000:
    #     st.session_state['content_tone'] = False

    my_markups()

    with checks[0]:
        rem_dup = st.checkbox('Remove Duplicates', disabled=False, label_visibility='visible', key='rem_dup')
        rem_pub = st.checkbox('Remove Publications', disabled=False, label_visibility="visible", key='rem_pub') 
        pub_tier = st.checkbox('Publication Tier', disabled=False, label_visibility="visible", key='pub_tier')
    with checks[1]:
        pub_edition =  st.checkbox('Publication Edition', disabled=False, label_visibility="visible", key='pub_edition')
        roi =  st.checkbox('ROI', disabled=False, label_visibility="visible", key='roi')
        content_tone =  st.checkbox('Tonality', label_visibility="visible", key='content_tone')
    with checks[2]:
        content_sum = st.checkbox('Summary', disabled=False, label_visibility="visible", key='summary_content')
        fav = st.checkbox('Favorability', label_visibility="visible", key='fav')
        rrc =  st.checkbox('Reach, Readership & Circulation', disabled=False, label_visibility="visible", key='rrc')
        # if file_size > 40000000:
        #     content_tone =  st.checkbox('Tonality', label_visibility="visible", disabled=False, key='content_tone')
        # else:
        #     content_tone =  st.checkbox('Tonality', label_visibility="visible", key='content_tone')
    # with checks[3]:
    #     topic_cluster =  st.checkbox('Topic Cluster', disabled=True, label_visibility="visible", key='topic_cluster')
        
    button_process_raw_file = st.button('Process Raw File')

    if button_process_raw_file:
        root_process(raw_file, rem_dup, rem_pub, pub_tier, pub_edition, rrc, roi, content_tone, fav, content_sum, fname, name)
    
    return


# main cleaner script
def main_cleaner(name):

    # st.header(f'🧹 Raw Cleaner')

    # Set the background image
    # bg_image()

    raw_file = st.file_uploader(label=':blue[Upload Raw File]:red[*]', type=["xls","xlsx"], key="raw_file", accept_multiple_files=False)

    if st.session_state['raw_file']:

        fname = st.text_input(label="Input Output Filename", key='fname')
        
        if fname:
            checkbox_select(raw_file, fname, name)
