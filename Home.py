import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pandas as pd
from Common import ui_settings, get_collection, is_valid_email, generate_password, passhash
import time

# tools
from Landing import landing_page
from Raw_Cleaner import main_cleaner
from Basic_Report import basic_report
from File_Merge import file_merger
from MMI_Wordcloud import word_cloud
from Add_Tonality import add_tonality
from Sharedview_Report import sv_report
from Report_Creator import report_landing
from Tools_Page import tools_landing
from Settings import settings_main

def main(name):

    # st.title(f'🛠️ :violet[*MMI Report Tools*]')

    authenticator.logout(button_name='Log out', location='sidebar')
    st.sidebar.title(f'🛠️ :violet[Report Tools]')
    st.sidebar.header(f':red[Welcome :blue[*{name.title()}*]] 👤')

    with st.sidebar:
        selected = option_menu(
            menu_title='Main',
            menu_icon='house-gear',
            options=['Home', 'Tools', 'Report Creator', 'SharedView Report', 'Settings'],
            icons=['house', 'tools', 'filetype-xlsx', 'filetype-xlsx', 'gear'],
            key='home_sidebar',
        )

        # st.caption(':red[Proverbs 21:21] \"Whoever pursues righteousness and love finds life, prosperity, and honor.\"')

    if selected == 'Home':
        landing_page()

    if selected == 'Tools':
        tools_landing(name)

    if selected == 'Report Creator':
        report_landing(name)
    
    if selected == 'SharedView Report':
        sv_report()
    
    if selected == 'Settings':
        settings_main()

    return


 
@st.dialog("Sign Up")
def dialog_signup():

    # --- Reset inputs before rendering if requested ---
    if "clear_inputs" in st.session_state and st.session_state.clear_inputs:
        for key in ['signup_username', 'signup_email']:
            st.session_state[key] = ''
        # st.session_state['item_size'] = 1
        # st.session_state['unit_size'] = 'GRAMS'
        st.session_state.clear_inputs = False
    with st.container(border=True):
        cols = st.columns([1, 3])
        with cols[0]:
            st.markdown('#### Username', help='Username should be 8 or more characters long...')
        with cols[1]:
            st.text_input(
                label='Username',
                label_visibility='collapsed',
                key='signup_username')
        
        cols = st.columns([1, 3])
        with cols[0]:
            st.markdown('#### Email', help='Use a valid email address...')
        with cols[1]:
            st.text_input(
                label='EMAIL',
                label_visibility='collapsed',
                key='signup_email')
    
    if len(st.session_state['signup_username']) >=8 and is_valid_email(st.session_state['signup_email']):
        if st.button('Submit', use_container_width=True):
            st.session_state.clear_inputs = True
            user_password = generate_password(12)
            user_hash = passhash(user_password)
            collection = get_collection('user')
            collection.insert_one({
                'username':st.session_state['signup_username'],
                'email':st.session_state['signup_email'],
                'hash':passhash(user_password)
            })


            with st.spinner('Processing....'):
                time.sleep(2)
                st.rerun()    
            


if __name__ == '__main__':

    # st.set_page_config(page_title="Media Meter Web Tool", initial_sidebar_state='expanded')
    ui_settings()

    with st.sidebar:
        collection = get_collection('user')

        # -----------username area-------------
        cols = st.columns([1, 3])
        with cols[0]:
            st.markdown('#### Username')
        with cols[1]:
            st.text_input(
                label='Username',
                label_visibility='collapsed',
                key='user_username')
            
        # -----------password area-------------
        cols = st.columns([1, 3])
        with cols[0]:
            st.markdown('#### Password')
        with cols[1]:
            st.text_input(
                label='Password',
                label_visibility='collapsed',
                key='user_password')
        
        cols = st.columns(2)
        with cols[0]:
            if st.button('Log In', use_container_width=True):
                ''''''
        with cols[1]:
            if st.button('Sign Up', use_container_width=True):
                dialog_signup()
        



    # Set the background image
    # bg_image()
    
    # st.header('With :red[GOD] all things are possible')
    # st.subheader('Matthew 19:26')
    # st.write('Jesus looked at them intently and said, “Humanly speaking, it is impossible. But with God everything is possible.”')


    # names = ['Jonathan Puray', 'Sheya Espaldon', 'Racquel Trillana', 'Andrea Joi Centeno', 'Ayessa Juraine Mancera', 'Ariza Alarcon', 'Paula Poblete', 'Mara Laya', 'Maria Anna Mae Paruan', 'Alvin Deocareza', 'Ayrone Masilungan', 'Christalline Llarena', 'Fritz Acebes', 'Christian Philip Lendio']
    # usernames = ['athan', 'sheyaesp', 'kelly', 'axcnn', 'amancera', 'amalarcon', 'pau', 'mcLaya', 'amaeparuan', 'adeocareza', 'vashy', 'talline', 'fritz', 'philip']

    # file_path = Path(__file__).parent/'support_files/hashed_pw.pkl'
    # with file_path.open('rb') as file:
    #     hashed_passwords=pickle.load(file)
    
    # credentials={
    #     "usernames":{
    #         usernames[0]:{
    #             "name":names[0],
    #             "password":hashed_passwords[0]
    #             },
    #         usernames[1]:{
    #             "name":names[1],
    #             "password":hashed_passwords[1]
    #             },
    #         usernames[2]:{
    #             "name":names[2],
    #             "password":hashed_passwords[2]
    #             },
    #         usernames[3]:{
    #             "name":names[3],
    #             "password":hashed_passwords[3]
    #             },
    #         usernames[4]:{
    #             "name":names[4],
    #             "password":hashed_passwords[4]
    #             },
    #         usernames[5]:{
    #             "name":names[5],
    #             "password":hashed_passwords[5]
    #             },
    #         usernames[6]:{
    #             "name":names[6],
    #             "password":hashed_passwords[6]
    #             },
    #         usernames[7]:{
    #             "name":names[7],
    #             "password":hashed_passwords[7]
    #             },
    #         usernames[8]:{
    #             "name":names[8],
    #             "password":hashed_passwords[8]
    #             },
    #         usernames[9]:{
    #             "name":names[9],
    #             "password":hashed_passwords[9]
    #             },
    #         usernames[10]:{
    #             "name":names[10],
    #             "password":hashed_passwords[10]
    #             },
    #         usernames[11]:{
    #             "name":names[11],
    #             "password":hashed_passwords[11]
    #             },
    #         usernames[12]:{
    #             "name":names[12],
    #             "password":hashed_passwords[12]
    #             },
    #         usernames[13]:{
    #             "name":names[13],
    #             "password":hashed_passwords[13]
    #             }       
    #         }
    #     }
    
    # authenticator = stauth.Authenticate(credentials, 'mmi_tool', 'abcdef', cookie_expiry_days=1)
    # name, authentication_status, username = authenticator.login(location='sidebar')

    # if authentication_status == False:
    #     st.sidebar.error('Username /password is incorrect')
    
    # if authentication_status == None:
    #     st.sidebar.warning('Please enter your username and password')
    
    # if authentication_status:
    #     main(name)
    
    # st.sidebar.caption(':red[Proverbs 21:21] \"Whoever pursues righteousness and love finds life, prosperity, and honor.\"')