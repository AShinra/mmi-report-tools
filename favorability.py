import streamlit as st
import pandas as pd


# favorability
def favorability(df):

    df['Favorability'] = ''
    df['Favorability'] = df['Favorability'].astype(str)
    df['Favorability Score'] = 0
    df['Favorability Score'] = df['Favorability Score'].astype(int)

    for i in df.index:

        mentions = df.at[i, 'Mention']
        tone = df.at[i, 'Tone']
        med_type = df.at[i, 'Media Type']

        if med_type in ["Radio", "TV"]:
            df.at[i, 'Favorability'] = 'For Manual Checking'
            df.at[i, 'Favorability Score'] = 0
        else:
            if mentions >= 3 and tone == 'Positive':
                df.at[i, 'Favorability'] = 'Significantly Positive'
                df.at[i, 'Favorability Score'] = 2
            elif mentions < 3 and tone == 'Positive':
                df.at[i, 'Favorability'] = 'Slightly Positive'
                df.at[i, 'Favorability Score'] = 1
            elif tone == 'Neutral':
                df.at[i, 'Favorability'] = 'Neutral'
                df.at[i, 'Favorability Score'] = 0
            elif mentions < 3 and tone == 'Negative':
                df.at[i, 'Favorability'] = 'Slightly Adverse'
                df.at[i, 'Favorability Score'] = -1
            elif mentions >= 3 and tone == 'Negative':
                df.at[i, 'Favorability'] = 'Significantly Adverse'
                df.at[i, 'Favorability Score'] = -2
    
    st.success(f'Added Favorability and Favorability Score')

    return df