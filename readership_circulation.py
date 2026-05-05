import streamlit as st
import pandas as pd

# add readership and circulation to print publications
def readership_and_circulation(df, _data):

    df['Readership'] = 0
    df['Circulation'] = 0

    for i in df.index:
        for k, v in _data.items():
            if df['Publication'][i] == k:
                df.at[i,'Readership'] = int(v['Readership'])
                df.at[i,'Circulation'] = int(v['Circulation'])
                break

    st.success('Readership and Circulation added for Print Publications')

    return df