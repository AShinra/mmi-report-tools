import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')


# adds summary column
def summarize_text(_text):

    sw = set(stopwords.words("english"))
    _words = word_tokenize(_text)

    freqTable = dict()                 
    for word in _words:               
        word = word.lower()                 
    
        if word in sw:                 
            continue                  
        
        if word in freqTable:                       
            freqTable[word] += 1            
        else:          
            freqTable[word] = 1
    
    sentences = sent_tokenize(_text)                 
    sentenceValue = dict()                     

    for sentence in sentences:               
        for word, freq in freqTable.items():              
            if word in sentence.lower():
                if word in sentence.lower():
                    if sentence in sentenceValue:                                 
                        sentenceValue[sentence] += freq                       
                    else:                       
                        sentenceValue[sentence] = freq                    

    sumValues = 0                        
    for sentence in sentenceValue:              
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))     

    summary = ''      

    for sentence in sentences:               
        # if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1 * average)):
            summary += sentence + " "

    return summary