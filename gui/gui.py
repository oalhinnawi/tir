# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:24:45 2019

@author: Omar
"""
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5 import QtCore, QtGui, uic
from skeleton import Ui_Form
from textblob import TextBlob
import json
import os
from pathlib import Path
from rake_nltk import Rake
from gensim.test.utils import common_corpus, common_dictionary
import gensim
import datetime
import gui_utils
import nltk
from nltk.corpus import stopwords 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from gensim.corpora import Dictionary
from collections import defaultdict
from gensim import corpora


class MyApp(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        
        some_date = QtCore.QDate(2010,1,1)
        self.dateEdit.setDate(some_date)
        self.setup_processing(r'C:\Users\Omar\Desktop\tir\tir\data\politics')
        self.model_check()



#        print(dt_string)
#        teehee=self.dateEdit.date()
#        print(teehee.fromString())
#        print(dir(self.dateEdit.date().fromString()))
        
    def model_check(self):
        self.model=gensim.models.LsiModel.load(r'C:\Users\Omar\Desktop\tir\lsi_model\model')
        self.dictionary=Dictionary.load_from_text(r'C:\Users\Omar\Desktop\tir\wikidump_wordids.txt.bz2')
        #dictionary = corpora.Dictionary(texts)
        
    
    def setup_processing(self,path):
        self.path=path
        self.start_button.clicked.connect(self.post_gen)
        self.next_post_button.clicked.connect(self.get_next_post)
#        self.day_gen=
        
        
#    def get_next_post(self):
    
    def process_text(self,date):
        
        self.get_dates_json(self,date)
        curr_post=next(self.post_gen(date))
        
        self.show_raw_text(curr_post['body'])
        self.classify_text(curr_post['title'])
    
    def show_raw_text(self,raw_text):
        self.raw_text_view.append(raw_text)
        
        
    
        
    def get_next_post(self):

        curr_post=next(self.iterator)
        
#        for curr_post in self.post_gen(data):
        self.topics_view.setText('')
        self.context_view.setText('')
        self.raw_text_view.setText('')
        
        
        
        self.show_raw_text(curr_post['title'])
        self.classify_text(curr_post['title'])
        self.get_context_keywords(curr_post['title'])
        self.get_topics(curr_post['title'])
        
    def classify_text(self,raw_text):
        blob=TextBlob(raw_text)
        print(blob.sentiment.polarity)
        
        if(blob.sentiment.polarity>0.0):
            sentiment='Positive'
        else:
            sentiment='Negative'
        
        self.sentiment_output.setText(sentiment)
        
    def get_context_keywords(self,data):
        r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

        r.extract_keywords_from_text(data)
        keywords=r.get_ranked_phrases()
        for keyword in keywords:
            self.context_view.append(keyword)
#        print(r.get_ranked_phrases())

    def get_topics(self,data):
        
#        count = CountVectorizer()
#        docs = np.array([data])
#        bag = count.fit_transform(docs)
#        print(bag)
        bag=self.dictionary.doc2bow(data.lower().split())
        topics=self.model[bag]
#        self.topics_view.append(topics)
        topics = sorted(topics, key=lambda x:x[1])
        print(topics)
        highest_one=topics[len(topics)-1]
        print(highest_one)
        model_outputs=self.model.show_topic(highest_one[0])
        for topic in model_outputs:
            self.topics_view.append(topic[0])
    
    
    def start_date(self,date):
                
        #Getting the date from the date editor and then getting it preprocessed
        
        self.dt=self.dateEdit.dateTime()
        
        self.dt_string = self.dt.toString(self.dateEdit.displayFormat())        
        
        date=gui_utils.date_to_text(self.dt_string)
        
        database="../data"
        sub="politics"
        fs="/"
        print(database,fs,sub,fs)
        true_path=database+fs+sub+fs+date
        
        index=0

        
        
        
    def post_gen(self):
                
        
        #Getting the date from the date editor and then getting it preprocessed
        
        self.dt=self.dateEdit.dateTime()
        
        self.dt_string = self.dt.toString(self.dateEdit.displayFormat())        
        
        date=gui_utils.date_to_text(self.dt_string)
        
        database="../data"
        sub="politics"
        fs="/"
        print(database,fs,sub,fs)
        true_path=database+fs+sub+fs+date
        with open(true_path) as stream:
            data=json.load(stream)
        self.iterator=iter(data)
      
    def dump_results_to_text(self):
        print('')
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
