# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:20:47 2019

@author: omar
"""

import pandas
from datetime import datetime




def get_post_frame(json_line):

    params=['user',
            'title',
            'body',
            'subreddit',
            'score',
            'num_replies',
            'timestamp',
            'post_id',
            'id',
            'parent_id',
            'tag'
            ]
            

        
    if 'author' in json_line:
        author=json_line['author']
    elif 'user' in json_line:
        author=json_line['user']
    else:
        author=json_line['name']

    if 'link_id' in json_line:
        post_id=json_line['link_id']
    else:
        post_id=json_line['id']

    if 'body' in json_line:
        body=json_line['body']
    elif "selftext" in json_line:
        body=json_line['selftext']
    else:
        body=""


    dict1={        
                        "user":author,
                        "title":json_line['title'],
                        "body":body,
                        "subreddit":json_line['subreddit'],
                        "score":json_line['score'],
                        "num_replies":json_line['num_comments'],
                        "timestamp":json_line['created_utc'],                                                                
                        "post_id":post_id,
                        "id":json_line['id'],
                        "parent_id":"N/A",
                        "tag":'post'
                        }
    
    return dict1
    
def get_comment_frame(json_line):
        
    if 'author' in json_line:
        author=json_line['author']
    elif 'user' in json_line:
        author=json_line['user']
    else:
        author=json_line['name']

    if 'link_id' in json_line:
        post_id=json_line['link_id']
    else:
        post_id=json_line['id']
        
    if 'body' in json_line:
        body=json_line['body']
    else:
        body=""

    if "parent_id" in json_line:
        parent_id=json_line["parent_id"]
    else:
        parent_id="N/A"
        
    dict1={
            "user":author,
            "subreddit":json_line['subreddit'],
            "score":json_line['score'],
            "num_replies":0,
            "timestamp":json_line['created_utc'],
            "title":"",
            "body":body,
            "post_id":post_id,
            "id":json_line['id'],
            "parent_id":parent_id,
            "tag":'comment'
            }

    return dict1
    
#Takes in an int repping a unix timestamp, returns the day string
def unix_to_day_string(unix_timestamp):
    date=datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')
    
    return date
    
    
if __name__=="__main__":
    
    unix_to_day_string(1284101485)
    