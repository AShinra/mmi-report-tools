import streamlit as st
import pandas as pd

# add edition column
def publication_edition(df, _data):

    for i in df.index:
        for k, v in _data.items():
            if df['Media Type'][i] == k:
                df.at[i,'Edition'] = v

    st.success('Publication Edition Column added')

    return df