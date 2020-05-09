# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 09:18:38 2020

@author: omar
"""
from flask import Flask
from flask_cors import CORS
from flask import request,Response
import sys
import json
app = Flask(__name__)
cors = CORS(app)

import process_day
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(send_email):

    port=465 #For SSL
    password=''
    
    #Create a secure SSL context
    context=ssl.create_default_context()
    
    #Message
    msg=MIMEMultipart()
    msg['Subject']='Analysis'
    msg['From']='projecttir490@gmail.com'
    msg['To']=send_email
    
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    server.login("projecttir490@gmail.com",password)
    part = MIMEBase('application', "octet-stream")
    
    part.set_payload(open("Analysis.pdf", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Analysis.pdf"')
    msg.attach(part)
    server.sendmail('projecttir490@gmail.com',send_email, msg.as_string())
    
#    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
#        server.login("projecttir490@gmail.com","projecttir")
#        #TODO:send email here
#    
#        server.sendmail("projecttir490@gmail.com","oalhinnawi@gmail.com",message)
        
        




@app.route('/analysis', methods=['GET','POST'])
def analyze_day():

    #Parse data from the request
    data=request.data
    data=data.decode("utf-8")
    json_data=json.loads(data)
    json_data=json_data['data']
    #Parse sub,date, and the users email
    subreddit=json_data['subreddit']
    date=json_data['date']
    email=json_data['email']
    
    process_day.process_day(date,subreddit)
    send_email(email)
    return("Success processing {} for sub: {} and sending to {}".format(date,subreddit,email))
    
    
#if __name__=="__main__":
#    send_email('oalhinnawi@gmail.com')