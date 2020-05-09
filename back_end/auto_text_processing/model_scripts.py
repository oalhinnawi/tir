# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:21:32 2019

@author: omar
"""
import gensim
from gensim.corpora import Dictionary
import os
from text_processor_utils import clean_text

def model_autoprocess(subreddit,text_array):
    path_to_models_folder='../models/'+subreddit+'/'
    path_to_model=path_to_models_folder+'model.model'
#    if(os.path.exists(path_to_model)):      
#        update_model(subreddit,text_array)
#    else:
#        create_model(subreddit,text_array)
    create_model(subreddit,text_array)

#The function that should run if the model doesn't exist already
def create_model(subreddit,text_array):
    
    #Path to the dictionary 
    path_to_dict=r'../models/wikidump_wordids/wikidump_wordids.txt'

    #Path to the folder full of models pertaining to certain subreddits
    path_to_models_folder='../models/'+subreddit+'/'
    
    #Path to where we're gonna save the model
    path_to_model=path_to_models_folder+'model.model'
    
    #TypeError: doc2bow expects an array of unicode tokens on input, not a single string
    clean_text_array=[clean_text(text) for text in text_array]
    #Cleaning up the text 
    #TypeError: coercing to str: need a bytes-like object, tuple found
    print(clean_text_array)
#    common_corpus = [dct.doc2bow(text) for text in clean_text_array]
    
    #Training the new model
    model=gensim.models.LdaModel(clean_text_array,num_topics=100,eval_every=1,passes=2,minimum_probability=0.05)
    
    #Save the new model
    model.save(path_to_model)
    
    
#The function that should run if the model does already exist
def update_model(subreddit,text_array):
    debug=False
    #Path to the dictionary 
    path_to_dict=r'../models/wikidump_wordids/wikidump_wordids.txt'

    #Path to the folder full of models pertaining to certain subreddits
    path_to_models_folder='../models/'+subreddit+'/'
    
    #Path to where we're gonna save the model
    path_to_model=path_to_models_folder+'model.model'
    path_to_load=path_to_models_folder+'model.model'
    #Load model
    model=gensim.models.LdaModel.load(path_to_load)
    
    #Loading in dictionary
    dct=Dictionary()
    dct.add_documents([text_array])
    id2word=dct
    #Cleaning up the text 
    common_corpus = [clean_text(text) for text in text_array]


    
    
    #Debug Print
    if debug:
        print(common_corpus)


    #Training the new model
    model.update(common_corpus)
    
    #Save the new model
    model.save(path_to_model)