import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl



def to_excel(df):

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='MERGED')
    writer.close()
    processed_data = output.getvalue()

    return processed_data


def file_merger():
    my_files = st.file_uploader(label=':blue[Upload Files to Merge]:red[*]', type=["xls","xlsx", "csv"], key="Demo", accept_multiple_files=True)

    if my_files == []:
        st.stop()
    else:
        if st.button('Merge Files'):

            my_frames = [f for f in my_files]

            try:
                df_frames = [pd.read_excel(i) for i in my_frames]
            except:
                df_frames = [pd.read_csv(i, encoding='iso-8859-1', on_bad_lines='skip') for i in my_frames]

            for _frame in df_frames:
                try:
                    _frame.rename(columns={'Bucket':'Company'}, inplace=True)
                except:
                    pass

                try:
                    _frame.rename(columns={'Link':'v3 - Link'}, inplace=True)
                except:
                    pass

                try:
                    _frame.rename(columns={'Raw Date':'Date'}, inplace=True)
                except:
                    pass

                try:
                    _frame.rename(columns={'Pr Value':'PR Value'}, inplace=True)
                except:
                    pass
                
                try:
                    _frame.rename(columns={'language':'Language'}, inplace=True)
                except:
                    pass

            merged_df = pd.concat(df_frames)

            # download dataframe to excel file
            st.success(f':red[NOTE:] Downloaded file will go to the :red[Downloads Folder]')
            df_xlsx = to_excel(merged_df)

            st.download_button(label='📥 Download Current Result', data=df_xlsx ,file_name= f'Merged_File.xlsx')