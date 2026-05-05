import pandas as pd
import nltk
import streamlit as st

@st.cache_resource
def nltkdownloads():
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    nltk.download('punkt')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
import re


def tonality(df):

    nltkdownloads()

    # add Tone Column
    df['Hit Sentences'] = ''
    df['Tone Score'] = ''
    df['Tone'] = ''

    # set stop words
    stops = set(stopwords.words('english'))

    # set sentiment analyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()

    for i in df.index:

        keyword = df['Keywords'][i].lower().split(',')
        try:
            content = df['Content'][i].lower()
        except:
            content = df['Title'][i].lower()

        content = re.sub(r'[^a-zA-Z0-9. ]', '', content)
        content = content.split('.')

        new_content = []
        marker = 0
        for sentence in content:
            for j in keyword:
                if j in sentence:
                    marker += 1
            if marker != 0:
                new_content.append(sentence)
            marker = 0

        
        df.at[i, 'Hit Sentences'] = new_content

        new_content = [word_tokenize(x) for x in new_content]
        
        for sentence in new_content:
            for _word in sentence:
                if _word in stops:
                    sentence.remove(_word)

        tone_score=0
        for sentence in new_content:
            sentence = ' '.join(sentence)
            senti = sentiment_analyzer.polarity_scores(sentence)
            sentence_count=0
            for k, v in senti.items():
                sentence_count += 1
                if k == 'compound':
                    tone_score += v
        
        # get the average the tonality
        try:
            tone_score = tone_score/sentence_count
        except:
            tone_score = 0

        if tone_score >= 0.05:
            df.at[i, 'Tone'] = 'Positive'
        elif tone_score <= -0.1:
            df.at[i, 'Tone'] = 'Negative'
        else:
            df.at[i, 'Tone'] = 'Neutral'
        
        df.at[i, 'Tone Score'] = tone_score
    
    st.success('Tonality Added')
        

    return df

        

   



   