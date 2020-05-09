# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:37:23 2020

@author: omar
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import smtplib, ssl
import sys
from PyQt5 import QtCore, QtGui, uic
from skeleton import Ui_Form
import json
import os
from pathlib import Path
import numpy as np
import pandas
import sys
sys.path.insert(0,'../models/')
import process_day

class MyApp(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.setup_buttons()
        
    def setup_buttons(self):
        self.start_analysis_button.clicked.connect(self.email_results)
    
    def process_date(self):
        #Get the date
        self.dt=self.dateEdit.dateTime()    
        self.dt_string = self.dt.toString(self.dateEdit.displayFormat())  
        date_string=self.date_to_text(self.dt_string)
        
        #Get the subreddit
        subreddit=self.subreddit_input.text()
        
        #Processing days
        process_day.process_day(date_string,subreddit)
    
    def email_results(self):
        print("jesus christ help me")
        message="""\
        Subject:TOPICS
---
        Topic 0:
        people way old say high movie things days attack obama
        Topic 1:
        10 don need let getting great set advice better 30
        Topic 2:
        years best new reddit eve 25 16 uk youtube job
        Topic 3:
        2016 really season gt change family fuck review 31 final
        Topic 4:
        2017 01 january removed night com home 11 02 jan
        Topic 5:
        question man friends party music song favorite thanks items trade
        Topic 6:
        time make black blue keys card 24 red fn self
        Topic 7:
        looking bitcoin https work painted player nye dog funny women
        Topic 8:
        post vs girl thread says 19 starting coming feel hours
        Topic 9:
        ps4 keys xbox offers white guy crimson heatwave purple zsr
        Topic 10:
        know trump play 15 killed hard working finally open players
        Topic 11:
        good today free guys watch times story real 100 girls
        Topic 12:
        amp does world love ft lf buy look oc store
        Topic 13:
        game 17 online bad end news questions sign used hot
        Topic 14:
        new year happy use irl star playing resolution mariah tips
        Topic 15:
        day m4f did think ve going sports long week house
        Topic 16:
        pc want games thing 12 win wheels pink discussion 21
        Topic 17:
        live little big 18 request small local men death baby
        Topic 18:
        just help like got right start life need friend team
        Topic 19:
        video 20 fun national list 22 come trying history la
        
---
        """
        port=465 #For SSL
        password='projecttir'
        
        #Create a secure SSL context
        context=ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
            server.login("projecttir490@gmail.com",password)
            #TODO:send email here
        
            server.sendmail("projecttir490@gmail.com","oalhinnawi@gmail.com",message)
        print("Email sent you virgins")
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