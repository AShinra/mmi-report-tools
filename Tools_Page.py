import streamlit as st
from streamlit_option_menu import option_menu
from Raw_Cleaner import main_cleaner
from Add_Tonality import add_tonality
from File_Merge import file_merger
from MMI_Wordcloud import word_cloud
from csv_to_excel import csv_to_excel

def tools_landing(name):

    with st.container(border=True):
        h_col1, h_col2 = st.columns([1,4])
        with h_col1:
            st.image('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3N2c2lldXNjM2c4dGozMTlmMnBrOG43Nzk2NTVveGRmMnpwdTk3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.webp', use_column_width=True)
        with h_col2:
            st.header(':toolbox: Tools', divider=True)

    with st.sidebar:
        selected = option_menu(
            menu_title='',
            options=['Cleaner', 'Converter', 'Tonality', 'Wordcloud'],
            icons=['magic', 'filetype-csv', 'file-music', 'cloud'],
            orientation='vertical',
            default_index=0
        )

    if selected == 'Cleaner':
        main_cleaner(name)
    elif selected == 'Converter':
        csv_to_excel(name)
    elif selected == 'Tonality':
        add_tonality()
    elif selected == 'Wordcloud':
        word_cloud()