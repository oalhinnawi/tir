# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:42:45 2019

@author: Omar
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import gensim
from gensim.corpora import Dictionary

#This function will tokenize,lemmatize, and stem text
def clean_text(text):
    #Stem the text
    ps=PorterStemmer()
    text=ps.stem(text)
    
    #Tokenize the f****** text
    text=word_tokenize(text)
    
    #path to dictionary
    path_to_dict=r'C:\Users\Omar\Desktop\tir\lsi_model\wikidump_wordids.txt'
    
    #Convert to a bag of words
    dct = Dictionary.load_from_text(path_to_dict)  
    # initialize a Dictionary
    
#    text=[text]
    
    #Called dictionary onto tokenized/stemmed text
    bow=dct.doc2bow(text)
    
    return bow
    
if __name__=='__main__':
    bow=clean_text('jesus christ please god help me')
    print(bow)
    model=gensim.models.LdaModel.load(r'C:\Users\Omar\Desktop\tir\lda_model\model.model')
    print(model.print_topics())
    topics=model[bow]
    print(topics)
    for vector,key in topics:
        print(vector)