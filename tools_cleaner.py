import json
import streamlit as st


# title cleaner added June 04, 2024
def title_cleaner(my_title, my_publication):

    _f = open(f'support_files/title_cleaner.json')
    _data = json.load(_f)

    my_title = my_title.lstrip()
    my_title = my_title.rstrip()
    cleaned_title = my_title

    for pub, for_deletions in _data.items():
        if my_publication == pub:
            for for_deletion in for_deletions:
                if (my_title.lower()).endswith(for_deletion.lower()):
                    myLen = len(for_deletion)
                    titleLen = len(my_title)
                    finLen = titleLen - myLen 
                    # st.write(my_title)
                    # cleaned_title = my_title.replace(for_deletion, "")
                    cleaned_title = my_title[:finLen]
                    cleaned_title = cleaned_title.lstrip()
                    cleaned_title = cleaned_title.rstrip()
                    # .write(cleaned_title)
                    break

    return cleaned_title


# remove publications from list
def remove_publications(df, _data):

    remove_list = _data['remove']

    orig_length = df.shape[0]

    drop_list = []

    for i in df.index:
        if df['Publication'][i] in remove_list:
            drop_list.append(i)  

    df = df.drop(drop_list)

    new_length = df.shape[0]

    removed_rows = orig_length-new_length

    st.success(f'Removed {removed_rows} Publications')

    return df


# publication name consistent
def consistent_pub(df, _data):

    for i in df.index:
        if df['Media Type'][i] in ['Online News', 'Blogs']: 
            for k, v in _data.items():
                if k in df['Article Source'][i] or v['Alt'] in df['Article Source'][i]:
                    df.at[i,'Publication'] = v['Pub_Name']
                    df.at[i,'Media Type'] = v['Type']
                    break

    return df