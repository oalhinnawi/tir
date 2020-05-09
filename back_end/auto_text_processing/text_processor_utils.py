# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:46:43 2019

@author: omar
"""
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import gensim
from gensim.corpora import Dictionary
#This function will tokenize,lemmatize, and stem text
def clean_text(text):
    debug=False
    #Stem the text
    if debug:
        print(text)
    ps=PorterStemmer()
    text=ps.stem(text)

    #Tokenize the f****** text
    text=word_tokenize(text)
    text=[word.lower() for word in text if word.isalpha()]

        
    #Removing Stopwrods    
    stop_words=set(stopwords.words('english'))
    reddit_stopwords=['[removed]','[deleted]']
    text=[w for w in text if not w in stop_words]
    text=[w for w in text if not w in reddit_stopwords]

    if debug:
        print(text)
    
#    #path to dictionary
    path_to_dict='../models/wikidump_wordids/wikidump_wordids.txt'
#    
#    #Convert to a bag of words

#    print("loading in a dictionary")
    dct = Dictionary.load_from_text(path_to_dict)  

    # initialize a Dictionary
#    dct=Dictionary(text)
#    text=[text]
    
    #Called dictionary onto tokenized/stemmed text
#    print('Converting to a bag of words')
    bow=dct.doc2bow(text)
    
    return bow

def date_to_text(date_string):
    
    raw=date_string.split("/")
    
    day = int(raw[1])
    
    month = int(raw[0])
    
    year = int(raw[2])
    
    if(day<10):
        day = str(day)
        day = "0"+day
    else:
        day = str(raw[1])
    
    
    if(month<10):
        month = str(month)
        month = "0"+month
    else:
        month = str(raw[0])

    
    year = str(raw[2])


    file=year+'-'+month+'-'+day+'.h5'
    print("We are looking at file: ",file)

    return file,year


if __name__ == "__main__":
    date_to_text("12/5/2010")
    