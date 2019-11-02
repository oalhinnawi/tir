# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 17:12:51 2019

@author: Omar
"""

import numpy as np 
import pandas as pd 
import re
import nltk 
import matplotlib.pyplot as plt



data_source_url = "https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv"
airline_tweets = pd.read_csv(data_source_url)


plot_size = plt.rcParams["figure.figsize"] 
print(plot_size[0]) 
print(plot_size[1])

plot_size[0] = 8
plot_size[1] = 6
plt.rcParams["figure.figsize"] = plot_size 

airline_tweets.airline.value_counts().plot(kind='pie', autopct='%1.0f%%')