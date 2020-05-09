# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 17:52:07 2019

@author: Omar
"""
import gensim
from text_preprocessing.clean_text import clean_text


model=gensim.models.LdaModel.load(r'model.model')

text=""
bow=clean_text(text)
print(bow)
topics=model.get_document_topics(bow)

for topic in topics:
    print(topic)

