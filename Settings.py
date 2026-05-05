import streamlit as st
from streamlit_option_menu import option_menu
import json


def settings_main():

    with st.sidebar:
        selected = option_menu(
            menu_title='',
            options=['Publications', 'Tool2', 'Tool3'],
            # icons=['house', 'wrench', 'filetype-xlsx'],
            key='settings_main',
            orientation='vertical'
        )
    
    if selected=='Publications':
        blacklisted_publication()


def blacklisted_publication():

    # open json file
    f = open('support_files/publications_remove.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # get options to use
    pub_options = data['remove']
    pub_options.sort()

    st.subheader('Blacklisted Publications')
    st.caption(':red[Warning! Modifying this area will affect all users]')
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(label='Blacklisted', key='remove_from_blacklist', options=pub_options, help='Blacklisted Publications')
            if st.session_state['remove_from_blacklist'] not in [None, '']:
                remove_pub = st.button('Remove', use_container_width=True)
                if remove_pub:
                    pub_options.remove(st.session_state['remove_from_blacklist'])
                    with open('support_files/publications_remove.json', "w") as outfile: 
                        json.dump(data, outfile)
                    st.success(f'Removed {st.session_state["remove_from_blacklist"]} from the blacklist')
        with col2:
            st.text_input(label='Add Publication to Blacklist', key='pub_add', help='Add Publication to be Blacklisted')
            if st.session_state['pub_add'] not in [None, '']:
                add_pub = st.button('Add', use_container_width=True)
                if add_pub:
                    pub_options.append(st.session_state['pub_add'])
                    with open('support_files/publications_remove.json', "w") as outfile: 
                        json.dump(data, outfile)
                    st.success(f'Added {st.session_state["pub_add"]} to the blacklist')
    
    

        
    

    return