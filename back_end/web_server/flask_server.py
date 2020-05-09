# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:43:35 2020

@author: omar
"""

from flask import Flask



app=Flask(__name__)

@app.route('/')

def hello_world():
    return "Hello, world"
    
    
def email_test('/test'):
    print()
def get_subreddit_analysis('/date/<date>/<subreddit>'):
    print