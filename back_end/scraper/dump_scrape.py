# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:02:07 2019

@author: Omar
"""

import bz2
import os
import pandas
import json
from dump_scrape_utils import get_post_frame,get_comment_frame,unix_to_day_string
import sys
import pprint
import logging

params=[
        'user',
        'subreddit',
        'score',
        'timestamp',
        'title',
        'body',
        'id',
        'tag'
        ]

subreddits=[
#        'the_donald',
        '2007scape'
#        'destiny2',
#        'Nest',
#        'ourpresident',
#        'wolves',
#        'politics'
        
        ]
'''
function that will scrape the dump of all files 

params:
    Year- the year that were interested in 
    Classification - Do we want the posts or the comments for that day
    Subreddit(s) -What is/are our sub(s) of interest?
    base_path - what is the base path of our dataframes (should ideally be the same as dump)
    dump_path what is the base dump path of our dataframes (should ideally be the same as dump)
'''

def dump_scrape(year,
                classification,
                subreddit,
                base_path='C:/Users/Omar/Desktop/hard_drive_tir/tir/tir/dataframe/',
                dump_path='C:/Users/Omar/Desktop/hard_drive_tir/tir/tir/dataframe/'):
    
    #Dump where we keep our raw unscraped data
    dump_path='raw_unseparated/'
    
    
    #Get all files in that year
    files=os.listdir(path)
    
    for file in files:
        file_path=path+file
        print(file_path)
        
        with bz2.open(file_path) as stream:
            for line in stream:
                line=line.decode("utf-8")
#                print(line)
#                sys.exit()
                try:
                    gg=json.loads(str(line))
                    #If the subreddit is in the list of reddits
                    if gg['subreddit'] in subreddit:    
                        '''
                        Determine if we're geting the comment frame 
                        or the posts frame
                        '''
                        if classification=='comment':
                            print(gg)
                            #Comment frame retrieval using helper function (more readable)
                            frame=get_comment_frame(gg)
                            #getting the day from the unix timestamp
                            time_string=unix_to_day_string(gg['created_utc'])
                            
                            #Adding date to the end of this for less complications
                            dump_path=base_dump_path+gg['subreddit']+'/'+time_string
                            
                                
                        else:
                            frame=get_post_frame(gg)
                            
                            #getting the day from the unix timestamp
                            time_string=unix_to_day_string(gg['created_utc'])
                            
                            #Adding date to the end of this for less complications
                            dump_path=base_dump_path+gg['subreddit']+'/'+time_string
                            
                            
                            if os.path.exists(dump_path):
                                print(gg['subreddit'])
                            else:
                                frame.to_hdf(dump_path,'post_data','a',format='table')                     
    
                            
                except Exception as e:
                    print(e)
    

if __name__=='__main__':
#    dump_scrape(2017,'post',subreddits)
    dump_scrape(2017,'comment',subreddits)
