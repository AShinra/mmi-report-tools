import streamlit as st
from streamlit_option_menu import option_menu
from Basic_Report import main
from Other_Reports.PR_Reports.BDO_CommSense.bdo_commsense import bdo_main, bdo_initial
from Other_Reports.Weekly_Reports.Foodpanda.foodpanda import foodpanda, foodpanda_initial
from Other_Reports.Weekly_Reports.OMD.omd import omd_initial
from SharedView import main_sv

def report_landing(name):

    # st.set_page_config(page_title="Report Creator", layout='wide')
    with st.container(border=True):
        h_col1, h_col2 = st.columns([1,4])
        with h_col1:
            st.image('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3N2c2lldXNjM2c4dGozMTlmMnBrOG43Nzk2NTVveGRmMnpwdTk3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.webp', use_column_width=True)
        with h_col2:
            st.header(':chart_with_upwards_trend: Report Creator', divider=True)

    cleaned_file = st.file_uploader(label=':blue[Upload Cleaned Xlsx File]:red[*]', type=["xls","xlsx"], key="cleaned_file", accept_multiple_files=False)
    
    with st.sidebar:
        selected = option_menu(
            menu_title='',
            options=['Basic', 'Daily', 'Weekly', 'Monthly', 'Annual', 'PR Report', 'SharedView'],
            icons=['file-bar-graph', 'calendar-day', 'calendar-week', 'calendar-month', 'calendar2', '', ''],
            orientation='vertical',
            default_index=0
        )

    if selected == 'Basic':
       if st.session_state['cleaned_file'] != None:
            main(st.session_state['cleaned_file'], name)
    
    elif selected == 'Daily':
        st.radio('Select Client', ['Client 1', 'Client 2'])
    
    elif selected == 'Weekly':
        tab2_cols_1, tab2_cols_2 = st.columns([1, 2])

        with tab2_cols_1:
            tab2_options = st.radio('Select Client',
                                    [
                                        'Foodpanda Philippines',
                                        'OMD Philippines'
                                    ], key='client_name2')
        with tab2_cols_2:

            if st.session_state['client_name2'] == "Foodpanda Philippines":
                foodpanda_initial(st.session_state['cleaned_file'])
            elif st.session_state['client_name2'] == "OMD Philippines":
                omd_initial(st.session_state['cleaned_file'])

    elif selected == 'Monthly':
        tab5_cols_1, tab5_cols_2 = st.columns([1, 2])

        with tab5_cols_1:
            with st.container(border=True):
                tab5_options = st.radio('Select Client',
                                        [
                                            'BDO-Comm&Sense',
                                            'PR Client 2'
                                        ], key='client_name5')
            
        with tab5_cols_2:
            with st.container(border=True):
                if st.session_state['client_name5'] == 'BDO-Comm&Sense':
                    if st.session_state['cleaned_file'] != None:
                        bdo_initial(st.session_state['cleaned_file'])
                    else:
                        st.error('Please upload raw file!')


    # tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Basic', 'Daily', 'Weekly', 'Monthly', 'Annual', 'PR Report', 'SharedView'])

    # with tab0:
    #     if st.session_state['cleaned_file'] != None:
    #         main(st.session_state['cleaned_file'], name)
    
    # with tab1:
    #     tab0_options = st.radio('Select Client',
    #                             [
    #                                 'Client 1',
    #                                 'Client 2'
    #                             ])
   
    # with tab2:
    #     tab2_cols_1, tab2_cols_2 = st.columns([1, 2])

    #     with tab2_cols_1:
    #         tab2_options = st.radio('Select Client',
    #                                 [
    #                                     'Foodpanda Philippines',
    #                                     'OMD Philippines'
    #                                 ], key='client_name2')
    #     with tab2_cols_2:

    #         if st.session_state['client_name2'] == "Foodpanda Philippines":
    #             foodpanda_initial(st.session_state['cleaned_file'])
    #         elif st.session_state['client_name2'] == "OMD Philippines":
    #             omd_initial(st.session_state['cleaned_file'])
            
    # with tab5:
    #     tab5_cols_1, tab5_cols_2 = st.columns([1, 2])

    #     with tab5_cols_1:
    #         with st.container(border=True):
    #             tab5_options = st.radio('Select Client',
    #                                     [
    #                                         'BDO-Comm&Sense',
    #                                         'PR Client 2'
    #                                     ], key='client_name5')
            
    #     with tab5_cols_2:
    #         with st.container(border=True):
    #             if st.session_state['client_name5'] == 'BDO-Comm&Sense':
    #                 if st.session_state['cleaned_file'] != None:
    #                     bdo_initial(st.session_state['cleaned_file'])
    #                 else:
    #                     st.error('Please upload raw file!')
        

    # with tab6:
        # if st.session_state['cleaned_file']!=None:
        #     main_sv(st.session_state['cleaned_file'], name)
    #     ''

    # return