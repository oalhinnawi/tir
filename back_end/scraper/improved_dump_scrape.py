# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:31:08 2020

@author: omar
"""

import os
import bz2
import sys
import csv
import pandas
import json
from dump_scrape_utils import get_post_frame, get_comment_frame,unix_to_day_string

params=['user',
        'subreddit',
        'score',
        'num_replies',
        'timestamp',
        'title',
        'body',
        'post_id',
        'id',
        'parent_id',
        'tag'
        ]

        
path='C:/Users/Omar/Desktop/back_end/data/raw_unseparated/post/'
dump_path='C:/Users/Omar/Desktop/back_end/data/days/post/'
files=os.listdir(path)

current_date="NONE"
fileobj=None
for year in range(2017,2018):
    
    year_path=path+str(year)+'/'
    dump_year_path=dump_path+str(year)+'/'
    files=os.listdir(year_path)
    for file in files:   
        file_path=year_path+file
        print(file_path)
        
        with bz2.open(file_path) as stream:
            for line in stream:
                line=line.decode("utf-8")
    
                
                
                try:
                    gg=json.loads(str(line))
    
                    #Open up a different file if one doesn't exist
                    if(current_date=="NONE"):
                        current_date=unix_to_day_string(int(gg['created_utc']))
                        fileobj=open(dump_year_path+current_date+'.csv','a',newline='',encoding="UTF-8")
                        csv_writer=csv.writer(fileobj)
                            
                    elif(current_date!=unix_to_day_string(int(gg['created_utc']))):
                        current_date=unix_to_day_string(int(gg['created_utc']))
                        fileobj.close()
                        fileobj=open(dump_year_path+current_date+'.csv','a',newline='',encoding='UTF-8')
                        csv_writer=csv.writer(fileobj)                
                  
                    #If the subreddit is in the list of reddits
                    dict1=get_post_frame(gg)


                    #Write data to the day file
                    csv_writer.writerow([dict1['user'],
                                        dict1['subreddit'],
                                        dict1['score'],
                                        dict1['num_replies'],
                                        dict1['timestamp'],
                                        dict1['title'],
                                        dict1['body'],
                                        dict1['post_id'],
                                        dict1['id'],
                                        dict1['parent_id'],
                                        dict1['tag']])
                        
                    
                except Exception as e:
                    print(e)


        