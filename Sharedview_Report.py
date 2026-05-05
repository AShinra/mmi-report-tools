import streamlit as st
from Sharedview_Dialog import show_dialog


def selection_popup():

    col1, col2 = st.columns(2)

    with col1:
        with st.form(key='form1'):
            with st.container(border=True):
                st.subheader('INFORMATION')
            
            with st.container(border=True):
                # client name
                st.text_input(label=':blue[Client Name]:red[*]', key='client_name')
                # report month
                st.selectbox(':blue[Report Month]:red[*]', key='report_month', options=
                                                [
                                                    'January',
                                                    'February',
                                                    'March',
                                                    'April',
                                                    'May',
                                                    'June',
                                                    'July',
                                                    'August',
                                                    'September',
                                                    'October',
                                                    'November',
                                                    'December'
                                                ])
                # report year
                st.number_input(label=':blue[Report Year]:red[*]', key='report_year', min_value=2000, value=2024)
            
            sub_fileinfo= st.form_submit_button('Submit Information', type='primary')

    
    with col2:
        with st.form(key='form2'):
            

            sub2 = st.form_submit_button('sub2')

    with st.container(border=True):
        st.subheader('REPORT SUMMARY')
        st.write(f'Client: {st.session_state["client_name"].title()}')
        st.write(f'Duration: {st.session_state["report_month"]} {st.session_state["report_year"]}')

    if sub_fileinfo and st.session_state['client_name']=='':
        st.error('ERROR: No client name')
    
    

    
    # if sub1:


    # with st.container(border=True):
    #     with st.popover('Report Information'):
    #         with st.form(key='data_form', border=False):
    #             form_columns = st.columns(3)
    #             with form_columns[0]:
    #                 fname = st.text_input(label=':blue[Client Name]:red[*]', key='client_name')
                
    #             with form_columns[1]:
    #                 report_month = st.selectbox(':blue[Report Month]:red[*]', key='report_month', options=
    #                                         [
    #                                             'January',
    #                                             'February',
    #                                             'March',
    #                                             'April',
    #                                             'May',
    #                                             'June',
    #                                             'July',
    #                                             'August',
    #                                             'September',
    #                                             'October',
    #                                             'November',
    #                                             'December'
    #                                         ])
    #             with form_columns[2]:
    #                 report_year = st.number_input(label=':blue[Report Year]:red[*]', key='report_year', min_value=2000, value=2024)
                
    #             sub_button = st.form_submit_button(label='Submit')

    # if st.session_state['client_name'] and st.session_state['report_month'] and st.session_state['report_year'] and sub_button:
    #     with st.container(border=True):
    #         col1, col2, col3 = st.columns(3)
    #         col1.write(f'CLIENT NAME: {st.session_state["client_name"]}')
    #         col2.write(f'REPORT DATE: {st.session_state["report_month"]}')
    #         col3.write(f'REPORT YEAR: {st.session_state["report_year"]}')

    #     with st.container(border=True):
    #         sub_button1 = st.button('Report Parameters')
    #         if sub_button1:
    #             with st.form():
    #                 st.write('Stest')
    #                 sub_button2 = st.form_submit_button('Testing')
    

    


def sv_report():

    st.header(f'📊 SharedView Report')

    cleaned_file = st.file_uploader(label=':blue[Upload SharedView Raw File]:red[*]', type=["xls","xlsx"], key="SVDemo", accept_multiple_files=False)

    if cleaned_file:
        selection_popup()
    else:
        st.stop()