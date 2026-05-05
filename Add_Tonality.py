import streamlit as st
from Tools import del_sheet1
from tonality import tonality
import pandas as pd
import openpyxl
from pathlib import Path



def add_tonality():
    my_file = st.file_uploader(label=':blue[Upload File]:red[*]', type=["xls","xlsx"], key="_file", accept_multiple_files=False)

    if st.session_state['_file']:

        my_fname = st.text_input(label="Output Filename", key='my_fname')

        if my_fname:

            button_add_tone = st.button('Process File', key='add_tone')

            if button_add_tone:
                
                df = pd.read_excel(my_file)
                df = tonality(df)

                REPORT_FILE = Path(__file__).parent/f'Temp_Files/Toned_{my_fname}.xlsx'
                wb = openpyxl.Workbook(REPORT_FILE)
                wb.save(REPORT_FILE)
                wb.close()

                writer = pd.ExcelWriter(REPORT_FILE, engine='openpyxl', mode='a')
                df.to_excel(writer, sheet_name='TONED', index=False)
                writer.close()

                # remove Sheet1
                REPORT_FILE = del_sheet1(REPORT_FILE)

                result_file = open(REPORT_FILE, 'rb')

                st.download_button(label='📥 Download Cleaned Raw', data=result_file ,file_name= f'Toned_{my_fname}.xlsx')

    return


