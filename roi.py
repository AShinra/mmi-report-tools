import streamlit as st
import pandas as pd


# add return of investment column
def roi_col(df):
    
    df['Hit(%)'] = 0
    df['Hit(%)'] = df['Hit(%)'].astype(float)
    # pd.to_numeric(df['Hit(%)'])
    df['ROI'] = 0
    df['ROI'] = df['ROI'].astype(float)
    # pd.to_numeric(df['ROI'])
    df['ROI_Value'] = 0
    df['ROI_Value'] = df['ROI_Value'].astype(float)
    df['ROI_in_M'] = 0
    df['ROI_in_M'] = df['ROI_in_M'].astype(float)
    df['PR_in_M'] = 0
    df['PR_in_M'] = df['PR_in_M'].astype(float)

    for i in df.index:
        if int(df['Mention'][i]) >= 20:
            _hit = 2
        else:
            _hit = int(df['Mention'][i])/10

        # df.at[i,'Hit(%)'] = "{:.0%}".format(_hit)
        # df.at[i,'Hit(%)'] = _hit*100
        df.at[i, 'Hit(%)'] = _hit

        # _roi = float(df['PR Value'][i]) * float(_hit)
        # df.at[i,'ROI'] = float("{:.2f}".format(_roi))
        _roi = df['PR Value'][i] * _hit
        df.at[i,'ROI'] = _roi

        # _roiv = float(1 + _hit) * float(df['PR Value'][i])
        # df.at[i,'ROI_Value'] = float("{:.2f}".format(_roiv))
        _roiv = (1 + _hit) * df['PR Value'][i]
        df.at[i,'ROI_Value'] = _roiv

        # _roim = float(df['ROI_Value'][i])/1000000
        # df.at[i,'ROI_in_M'] = "{:.2f}".format(_roim)
        _roim = df['ROI_Value'][i]/1000000
        df.at[i, 'ROI_in_M'] = _roim

        # _prm = float(df['PR Value'][i])/1000000
        # df.at[i,'PR_in_M'] = "{:.2f}".format(_prm)
        _prm = df['PR Value'][i]/1000000
        df.at[i, 'PR_in_M'] = _prm

    st.success('ROI Column Added')

    return df