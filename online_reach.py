import streamlit as st
import pandas as pd


# add reach for online and blog sites
def monthly_reach(df, _data):
    
    df['Monthly_Reach'] = 0
    df['Monthly_Reach'] = df['Monthly_Reach'].astype(float)

    for i in df.index:
        for k, v in _data.items():
            if k in df['Article Source'][i] or v['Alt'] in df['Article Source'][i]:
                df.at[i,'Monthly_Reach'] = float(v['Reach'])
                break

    st.success('Monthly Reach added for Online and Blogs')

    return df