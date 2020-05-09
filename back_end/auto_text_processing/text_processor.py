# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:41:13 2019

@author: Omar
"""
import sys
from rake_nltk import Rake
from gensim.models.ldamodel import LdaModel
import text_processor_utils
import pandas as pd
from gensim.corpora import Dictionary
from textblob import TextBlob
import time
import model_scripts   
from text_processor_utils import clean_text
import traceback
import pprint
import gensim
import operator
import datetime
'''
Get the titles, body, and comments
'''
#%%
def get_text_array(date,subreddit):

    hdf5_file,year=text_processor_utils.date_to_text(date)
    print(hdf5_file)
    date_path='C:/Users/omar/Desktop/hard_drive_tir/tir/tir/dataframe/'
    post_date_path=date_path+year+'/'+'post/'+'subreddits/'+subreddit+'/'+hdf5_file
    print(post_date_path)
    
    comment_date_path=date_path+year+'/'+'comment/'+'subreddits/'+subreddit+'/'+hdf5_file
    
    #Text Array to append to
    title_array=[]
    
    #Body array to append to
    body_array=[]

    #Comment Array to append to
    comment_array=[]    


    #User array for getting unique users 1
    user_array=[]
    
    
    #Open up the post store and retrieve the text
    store=pd.HDFStore(post_date_path)
    
    #Post keys
    keys=store.keys()
    
    #retrieve each of our posts
    print('pulling from posts')
    for key in keys:
        try:
            #Get the child object
            temp_df=store.get('/'+key)
            
            #Get the text from each child objects
            title=temp_df['title'].tolist()
            body=temp_df['body'].tolist()
            user=temp_df['user'].tolist()
            #Add the title and body together to append to text array
            title_array.append(title[0])
            print('BODY BODY BODY BODY')
            print(body[0])
            #If there was a body, append it to the list
            if body[0] != '':
#                print(body[0])
                body_array.append(body[0])
            else:
                print('No Body')
                
            #Get our list of users
            user_array.append(user[0])
        except:
            print('Post Key Error')
            traceback.print_exc(file=sys.stdout)
    #retrieve each of the comments
#    store=pd.HDFStore(comment_date_path)
    #Comments keys
#    keys=store.keys()
    print('Pulling from the comments')
#    for key in keys:
    try:
        print('FROM THE COMMENTS')
        #Get the child object
#        temp_df=store.get(key)
        df=pd.read_hdf(comment_date_path,'comment_data')
        #Get the text from each child objects
        comment_body_arr=df['body'].tolist()
        commment_user_arr=df['user'].tolist()
        
        #If there was a body, append it to the list
        for body in comment_body_arr:
            comment_array.append(body)
            
        #Get our list of users
        for user in commment_user_arr:
            user_array.append(user)
    except Exception as e:
        print(e)
        print('Comment Key Error')
    
        
    print("TITLE ARRAY \n\n",title_array)
    print("BODY ARRAY \n\n",body_array)
    print("COMMENT ARRAY \n\n",comment_array)
        
    return title_array,body_array,user_array,comment_array
    

#%%    
'''
Returns a positive neutral or negative sentiment

'''
def classify_text(raw_text):
    blob=TextBlob(raw_text)
    print(blob.sentiment.polarity)
    polarity=blob.sentiment.polarity
    
    #More detailed sentiment output
    #0.15 to -0.15 will be considered neutral
    if(polarity>=0):
        if(polarity<=1 and polarity>0.7):
            sentiment='Extremely Positive'
        elif(polarity<=0.7 and polarity>0.4):
            sentiment='Very Positive'
        elif(polarity<=0.4 and polarity>0.15):
            sentiment='Positive'
        else:
            sentiment='Neutral'
    else:
        if(polarity>=-1 and polarity<-0.7):
            sentiment='Extremely Negative'
        elif(polarity>=-0.7 and polarity<-0.4):
            sentiment='Very Negative'
        elif(polarity>=-0.4 and polarity<-0.15):
            sentiment='Negative'
        else:
            sentiment='Neutral'
        

    return(sentiment,polarity)
#%%
def get_context_keywords(data):
    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
    keyword_dict={}
    for string in data:
        
        r.extract_keywords_from_text(string)
        keywords=r.get_ranked_phrases()
        for keyword in keywords:
            if keyword in keyword_dict:
                keyword_dict[keyword]+=1
            else:
                keyword_dict[keyword]=1
    pprint.pprint(keyword_dict)
    keyword_list = dict(sorted(keyword_dict.items(), key=operator.itemgetter(1), reverse=True)[:30])
    return keyword_list

#        print(r.get_ranked_phrases())
#%%
def get_topics(subreddit,data):
    #politics
    bag_list=[clean_text(text) for text in data]
#    print(bag_list)
    
    #Path to the folder full of models pertaining to certain subreddits
    path_to_models_folder='../models/'+subreddit+'/'
    
    #Path to where we're gonna save the model
    path_to_model=path_to_models_folder+'model.model'
    path_to_load=path_to_models_folder+'model.model'
    
    #Load in the model
    model=gensim.models.LdaModel.load(path_to_load)
    all_topics=[]
    for bag in bag_list:
        topics=model[bag]
#        print(topics)
        all_topics.append(topics)
#        self.topics_view.append(topics)
    topics = sorted(topics, key=lambda x:x[1])
#    print(len(topics))
    highest_one=topics[len(topics)-1]
    model_outputs=model.show_topic(highest_one[0])
    topic_list=[]
    for topic in model_outputs:
        topic_list.append(topic[0])
        
    #dictionary path
    dct=Dictionary.load_from_text('../models/wikidump_wordids/wikidump_wordids.txt')
    topic_words=[]
    
    for topic in topic_list:
        topic_words.append(dct[int(topic)])
    return topic_words
#%%
def get_neg_pos(title_array,body_array,comment_array):

    #Initing stuff
    sent_dict={
               #Averages
               "avg_pos_score_post":0,
               "avg_neg_score_post":0,
               
               "avg_pos_score_com":0,
               "avg_neg_score_com":0,
               
               "avg_polarity_post":0,
               "avg_polarity_com":0,
               "avg_polarity_overall":0,
               
               "avg_post_length":0,
               "avg_title_length":0,              
               
               #Posts/comments
               "posts":0,
               "comments":0,
               
               
               #Total
               "total_pos_posts":0,
               "total_neg_posts":0,
               
               "total_pos_com":0,
               "total_neg_com":0,
               
               "total_pos_overall":0,
               "total_neg_overall":0
               
               }
    #length of title should be the equivalent of how many posts there were
    sent_dict['posts']=len(title_array)
    
    #Getting the number of comments from today
    sent_dict['comments']=len(comment_array)
    #%%
    #For each title in the title array
    
    for title,body in zip(title_array,body_array):
        print(title,body)
#        Run a sentiment analysis on the title and body
        sentiment,polarity=classify_text(title+body)
        #Add polarity to the 
        sent_dict['avg_polarity_post']+=polarity
        sent_dict['avg_polarity_overall']+=polarity
        #Adding sentiment to the scores to calc later
        #Positive
        if(polarity>0.15):
            sent_dict['avg_pos_score_post']+=polarity
            sent_dict['total_pos_posts']+=1
            sent_dict['total_pos_overall']+=1
        #Negative
        elif(polarity<-0.15):
            sent_dict['avg_neg_score_post']+=polarity
            sent_dict['total_neg_posts']+=1
            sent_dict['total_neg_overall']+=1
        
        #Add to the overall length right now then calc later on
        print("The length of the title was: ",len(title))
        print("The length of the body was: ",len(body))

        sent_dict['avg_title_length']+=len(title)
        sent_dict['avg_post_length']+=len(body)        
    #%%
    #For each comment in the comment_array
    for comment in comment_array:
        
        #Run a sentiment analysis
        sentiment,polarity=classify_text(comment)
        
        #Add polarity to the 
        sent_dict['avg_polarity_com']+=polarity
        sent_dict['avg_polarity_overall']+=polarity
        #Check the polarity
        #Positive
        if polarity>0.15:
            #If positive add to the total num of pos comments
            sent_dict['total_pos_com']+=1

            #add to the avg_pos (we'll div later)
            sent_dict["avg_pos_score_com"]+=polarity
        #Negative
        elif polarity<-0.15:
            #Else add to total negative comments
            sent_dict['total_neg_com']+=1
           
             #add to the avg_neg (we'll div later)
            sent_dict["avg_neg_score_com"]+=polarity  

    #Getting average pos/neg for posts
    pprint.pprint(sent_dict)
    if(sent_dict["posts"]!=0):
        sent_dict["avg_pos_score_post"]=sent_dict["avg_pos_score_post"]/sent_dict["posts"]
        sent_dict["avg_neg_score_post"]=sent_dict["avg_neg_score_post"]/sent_dict["posts"]
        #Getting overall polarity for both
        sent_dict["avg_polarity_post"]=sent_dict["avg_polarity_post"]/sent_dict["posts"]    
        #Getting avg lengths for both posts and comments
        sent_dict["avg_post_length"]=sent_dict["avg_post_length"]/sent_dict["posts"]    
        sent_dict["avg_title_length"]=sent_dict["avg_title_length"]/sent_dict["posts"]    

    if(sent_dict["comments"]!=0):
        #Getting average pos/neg for comments
        sent_dict["avg_pos_score_com"]=(sent_dict["avg_pos_score_com"]/sent_dict["comments"] )   
        sent_dict["avg_neg_score_com"]=(sent_dict["avg_neg_score_com"]/sent_dict["comments"])    
        sent_dict["avg_polarity_com"]=(sent_dict["avg_polarity_com"]/sent_dict["comments"])
    
    if(sent_dict["posts"]!=0 and sent_dict["comments"]!=0):
        sent_dict["avg_polarity_overall"]=sent_dict["avg_polarity_overall"]/(sent_dict["posts"]+sent_dict["comments"])   

        #Make totals for overall pos and neg instances
    sent_dict["total_pos_overall"]=(sent_dict["total_pos_posts"]+sent_dict["total_pos_com"])
    sent_dict["total_neg_overall"]=(sent_dict["total_neg_posts"]+sent_dict["total_neg_com"])

    return sent_dict
    

def write_info_to_dict(sent_dict):
    print('write info to dict')
    text_dict={
    "avg_pos":0.20,
    "avg_neg":-0.07,
    "avg_polarity":0.03,
    "avg_post":217,
    "avg_title":113,
    "date_unix":1483228800,
    "date":"2017-01-01",
    "posts":17,
    "comments":13,
    "total_pos":31,
    "total_neg":54,
    "most_common_topic":["Basketball","Sport","Lebron James"],
    "keywords":["Finals","National Basketball Association"],
    "subreddit":"nba"
               }

    
#%%
#EVerything here needs to get integrated into the auto_process.py script.
def day_autoprocess(day,subreddit):
    
    #Get all titles,bodys,comments,and
    title_array,body_array,user_array,comment_array=get_text_array(day,subreddit)
    
    #Making a cumulative text array
    cumulative_text=title_array+body_array+comment_array
    
    #Do the model check
    model_scripts.model_autoprocess(subreddit,cumulative_text)
    
    #Getting the topics of our text
    topics=get_topics(subreddit,cumulative_text)
    
    #Get the context keywords
    print("THIS IS WHATS GOING INTO THE KEYWORD GEN")
    print(cumulative_text)
    context_keywords=get_context_keywords(cumulative_text)
    print(context_keywords)
    #Get Neg/Pos Statistics
    sent_dict=get_neg_pos(title_array,body_array,comment_array)
    print(sent_dict)
    sent_dict['topics']=topics
    sent_dict['keywords']=context_keywords
    sent_dict['date_unix']=time.mktime(datetime.datetime.strptime(day, "%d/%m/%Y").timetuple())
    '''
    TODO:
        Make another dict that puts in:
            Topics
            Context Keywords
            Date
            Subreddit
    '''
    
    print(topics)
    
    with open('results.txt','a+') as stream:
        #Write out the results 
        stream.write(str(sent_dict)+'\n')
        
        
#%%
if __name__=='__main__':
    day='01/01/2017'
    
    subreddit='2007scape'
    day_autoprocess(day,subreddit)
            
