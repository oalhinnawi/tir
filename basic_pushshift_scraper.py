# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 10:14:43 2019

@author: Omar
"""


#Standard Python imports
import json
import os

#Pushshift imports
import psaw
from psaw import PushshiftAPI

#Time/Date imports
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta


def getComments(link,api,num_comments):
    comments=api.search_comments(link=link,
                                 sort_type='score',
                                 sort='desc',
                                 limit=num_comments)
    com_array=[]
    for comment in comments:
        com_array={
            "score":comment.score,
            "body":comment.body,
            "time_created":comment.created
            
        }    
    return com_array


def dumpJson(path,data):
    with open(path,'w+') as f:
        json.dump(data,f)

'''
Pushshift has a request limit of about 
1 request per 2 seconds (30 per minute)
'''


#Dump Folder Path
root_path='data/'


#Array of subreddits to scrape from
subs=[
      'politics'
      ]

#Number of posts (min:0, max:500 per search)
num_posts=3

#comments (not entirely sure what min/max are)
num_comments=1


#Initializing the api for use
api = PushshiftAPI()

#start_date=
#end_date=

#Get dates in between


for sub in subs:
    
    path=os.path.join(root_path+sub)+'/'
    
    #Making the request
    submissions = api.search_submissions(subreddit=sub,
                                         limit=num_posts,
                                         sort_type='score',
                                         sort='desc')
    
    index=0
    
    post_content=[]
    #For the number of posts that we can query from the search...
    for submission in submissions:
        comms_array=[]
        comms_array=getComments(submission.id,api,num_comments)
        
        if hasattr(submission,'body'):
            body=submission.body
        else:
            body='N/A'
        
        #print for sanity check
        post_content.append({
            "score":submission.score,
            "id":submission.id,
            "link":submission.permalink,
            "num_comms":submission.num_comments,
            "time_created":submission.created,
            "title":submission.title,
            "body":body,
            "comments":comms_array
        })
        print(post_content)
    
    dumpJson(path+'test.txt',post_content)




    
