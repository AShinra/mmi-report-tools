import streamlit as st
import pandas as pd

# add publication tier column
def publication_tier(df, _data):

    tier1_lists = [v for k, v in _data.items()]
    tier1_list = []
    for t_list in tier1_lists:
        for t in t_list:
            tier1_list.append(t)
    
    for i in df.index:
        for k, v in _data.items():
            if df['Publication'][i] in tier1_list:
                df.at[i,'Pub_Tier'] = 1
            else:
                df.at[i,'Pub_Tier'] = 2
    
    st.success('Publication Tier Column added')

    return df