import streamlit as st
from wordcloud import WordCloud
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import string
import json


def wc(df, REPORT_FILE, main_cat, fname):

    # get stopwords from json file
    f  = open('support_files/wc_stopwords.json')
    fl = json.load(f)
    stopwords = fl['STOPWORDS']


    # word frequency
    filtered_df = df.query('Category in @main_cat')
    _contents = filtered_df['Content'].to_list()
    contents = ''
    for _content in _contents:
        contents += ' '
        contents += _content

    text_content = contents.replace('\n', ' ')

    word_frequency = {}
    new_word_list = []
    for _word in text_content.split(' '):
        _word = _word.translate(str.maketrans('', '', string.punctuation)).lower()
        if _word != '':
            if _word not in stopwords:
                new_word_list.append(_word)
    
    _word_list = list(dict.fromkeys(new_word_list))
    _word_list = [x for x in _word_list if type(x) != int]
    _word_list = [x for x in _word_list if x.isdigit() == False]
    _word_list = [x for x in _word_list if x.isalnum() == True]
    
    for _word in _word_list:
        word_frequency[_word] = new_word_list.count(_word)

    word_frequency = dict(sorted(word_frequency.items(), key=lambda x:x[1], reverse=True))

    mask = np.array(Image.open('wc_patterns/circle2.png'))
  
    wordcloud = WordCloud(
                    width = mask.shape[1],
                    height = mask.shape[0],
                    background_color ='white',
                    stopwords = stopwords,
                    max_font_size = 250,
                    min_font_size = 10,
                    max_words=100,
                    font_path='wc_fonts/Benne-Regular.otf',
                    prefer_horizontal=1,
                    mask=mask
                    ).generate_from_frequencies(frequencies=word_frequency)
    
    # plot the WordCloud image                      
    # plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # plt.tight_layout(pad = 0)
    
    # plt.show()
    wordcloud.to_file('Temp_Files/wc.png')
    # st.image('Temp_Files/wc.png')

    wb = openpyxl.load_workbook(REPORT_FILE)
    wb.create_sheet('Wordcloud')
    ws_cloud = wb['Wordcloud']

    img = openpyxl.drawing.image.Image('Temp_Files/wc.png')
    img.anchor = 'A5'
    ws_cloud.add_image(img)

    ws_cloud['A2'].value = f'Words associated with {fname.upper()}'

    wb.save(REPORT_FILE)
    wb.close()

    return


# def word_cloud():
#     # st.set_page_config(page_title="Wordcloud", layout='wide')
#     # st.header(f'☁️ Wordcloud')
    
#     # Set the background image
#     # bg_image()

#     # raw_file = st.file_uploader(label=':blue[Upload File]:red[*]', type=["xls","xlsx"], key="Demo", accept_multiple_files=False)
#     data = st.text_area(label='Paste Text Here', key='clouddata')

#     if st.session_state['clouddata'] != '':
    
#         button_wc_process = st.button(label='Create Word Cloud')

#         if button_wc_process:
#             wc(data)


