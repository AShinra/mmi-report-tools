import streamlit as st


def landing_page():

    with st.container(border=True):
        h_col1, h_col2 = st.columns([1,4])
        with h_col1:
            st.image('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3N2c2lldXNjM2c4dGozMTlmMnBrOG43Nzk2NTVveGRmMnpwdTk3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.webp', use_container_width=True)
        with h_col2:
            st.header(':coffee: Welcome', divider=True)

    with st.container(border=True):
        tab0, tab1 = st.tabs(['🏠Home', '❓About'])

        tab0.write('🛠️Updates')
        tab0.write('⁜ October 12, 2024 - Added CSV to Excel Converter')
        tab0.write('⁜ October 02, 2024 - Added WordCloud to Basic Report')
        tab0.write('⁜ July 16, 2024 - Transfered all reports to Report Creator Page')
        tab0.write('⁜ July 16, 2024 - Created Report Creator Page')
        tab0.write('⁜ July 15, 2024 - Added Foodpanda Weekly Report in Other Reports')
        tab0.write('⁜ July 12, 2024 - Added favorability metrics')
        tab0.write('⁜ June 25, 2024 - Optimized FileMerger, fixed column name problem')
        tab0.write('⁜ June 20, 2024 - Removed leading and trailing spaces in title')
        tab0.write('⁜ June 20, 2024 - csv and excel file can be processed in Raw Cleaner')
        tab0.write('⁜ June 05, 2024 - Development of BDO Comm&Sense Report')
        tab0.write('⁜ June 04, 2024 - Added Title Cleaner in Raw Cleaner')
        tab0.write('⁜ May 01, 2024 - Updated Monthly Reach and Circulation')
        tab0.write('⁜ April 25, 2024 - Word CLoud Functional and ready to use')
        tab0.write('⁜ April 01, 2024 - Basic Report done')
        
        tab1.write('⁜ These tools were developed to improve the efficieny and speed of creating reports for Media Meter clients')

    

    
    
    return