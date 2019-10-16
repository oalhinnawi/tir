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

 
 
class MyApp(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.show_raw_text("Fuck the federal agents")
        self.classify_text("Fuck the federal agents")
    
    
    def process_date(self,date):
        self.get_dates_json(self,date)
    
    
    def show_raw_text(self,raw_text):
        self.raw_text_view.append(raw_text)
        
        
    def get_next_post(self):
        
        print("Getting next post")
        
        
    def classify_text(self,raw_text):
        blob=TextBlob(raw_text)
        print(blob.sentiment.polarity)
        
        if(blob.sentiment.polarity>0.0):
            sentiment='Positive'
        else:
            sentiment='Negative'
        
        self.sentiment_output.setText(sentiment)
        
        
    def get_dates_json(self,date):
        print(date)
        
        database=""
        sub=""
        fs="/"
        
        true_path=database+fs+sub+fs+date
        with open(true_path) as stream:
            data=json.load(stream)
            
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
