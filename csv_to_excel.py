import streamlit as st
import pandas as pd
import openpyxl
from pathlib import Path
from Tools import del_sheet1


def csv_to_excel(name):
    
    c_file = st.file_uploader(label=':blue[Upload CSV File]:red[*]', type=["csv"], key="csv_file", accept_multiple_files=False)

    if st.session_state['csv_file'] not in [None, '']:

        _filename = st.text_input(label='Input Filename', key='file_name')

        if st.session_state['file_name'] not in [None, '']:
            
            csv_button = st.button('Convert CSV')

            if csv_button:

                df = pd.read_csv(c_file, encoding='utf-8')
                df.reset_index(drop=True, inplace=True)

                _file = Path(__file__).parent/f'Temp_Files/excel_{name}.xlsx'
                wb = openpyxl.Workbook(_file)
                wb.save(_file)
                wb.close()

                try:
                    writer = pd.ExcelWriter(_file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
                    df.to_excel(writer, sheet_name='Sheet', index=False)
                    writer.close()
                except:
                    writer = pd.ExcelWriter(_file, engine='xlsxwriter')
                    df.to_excel(writer, sheet_name='Sheet', index=False, strings_to_urls=False)
                    writer.close()
                finally:
                    result_file = open(_file, 'rb')
                    st.success(f':red[NOTE:] Downloaded file will go to the :red[Downloads Folder]')
                    st.download_button(label='📥 Download Cleaned Raw', data=result_file ,file_name= f'{_filename}.xlsx')

    