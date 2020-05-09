# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:24:45 2019

@author: Omar
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

import sys
from PyQt5 import QtCore, QtGui, uic
from skeleton import Ui_Form
from textblob import TextBlob
import json
import os
from pathlib import Path
from rake_nltk import Rake
import numpy as np
import pandas


class MyApp(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        #FOR DEBUGGING
        self.subreddit_input.setText('2007scape')
        
        
        #Setting Date to some arbitrary date
        some_date = QtCore.QDate(2017,1,1)
        self.dateEdit.setDate(some_date)
        
        #Setting up the pipeline
        self.setup_processing()
   
    def setup_processing(self):        
        self.start_button.clicked.connect(self.retrieve_results)
#        self.next_post_button.clicked.connect(self.get_next_post)
#        self.auto_process_button.clicked.connect(self.process_day)
        
        
    def process_day(self):
        print('Im having a good time')
#    def get_next_post(self):
    def retrieve_results(self):
#        print(dir(self.subreddit_input))
        path_to_results='C:/Users/Omar/Desktop/hard_drive_tir/tir/tir/results/'+self.subreddit_input.text()+'/'
        self.dt=self.dateEdit.dateTime()
        
        self.dt_string = self.dt.toString(self.dateEdit.displayFormat())  
        date_string=self.date_to_text(self.dt_string)
        
        
        with open(path_to_results+date_string) as stream:
            for line in stream:
                print(line)
                line=line.replace("'",'"')
                print(line)

                gg=json.loads(line)

        self.avg_pos_score_com_output.setText(str(gg['avg_pos_score_com']))
        self.avg_neg_score_com_output.setText(str(gg['avg_neg_score_com']))
        self.avg_pos_score_post_output.setText(str(gg['avg_pos_score_post']))
        self.avg_neg_score_post_output.setText(str(gg['avg_neg_score_post']))
        self.avg_post_polarity_output.setText(str(gg['avg_polarity_post']))
        self.avg_com_polarity_output.setText(str(gg['avg_polarity_com']))
        self.avg_polarity_overall_output.setText(str(gg['avg_polarity_overall']))
        self.avg_post_length_output.setText(str(gg['avg_post_length']))
        self.avg_title_length_output.setText(str(gg['avg_title_length']))
        self.total_post_output.setText(str(gg['posts']))
        self.total_com_output.setText(str(gg['comments']))
        self.total_pos_post_output.setText(str(gg['total_pos_posts']))
        self.total_neg_post_output.setText(str(gg['total_neg_posts']))
        self.total_pos_com_output.setText(str(gg['total_pos_com']))
        self.total_neg_com_output.setText(str(gg['total_neg_com']))
        self.total_positive_output.setText(str(gg['total_pos_overall']))
        self.total_negative_output.setText(str(gg['total_neg_overall']))

        for topic in gg['topics']:
            print(topic)
            self.topics_view.append(topic)
            
        for keyword in gg['keywords']:
            print(keyword)
            self.context_view.append(keyword)
        
    def date_to_text(self,date_string):
        
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
    
    
        file=year+'-'+month+'-'+day+'.txt'
        print("We are looking at file: ",file)
    
        return file 
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
