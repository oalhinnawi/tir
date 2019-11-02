# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:19:34 2019

@author: Omar
"""


'''
Function that will take in the string representation 
and return the text file path 

e.g. 1/2/2010 -> 2010-01-02.txt

'''
def date_to_text(date_string):
    
    raw=date_string.split("/")
    
    day = int(raw[1])
    
    month = int(raw[0])
    
    year = int(raw[2])
    
    if(day<10):
        day = str(day)
        day = "0"+day
    else:
        day = str(raw[1])
    
    
    if(month<10):
        month = str(month)
        month = "0"+month
    else:
        month = str(raw[0])

    
    year = str(raw[2])


    file=year+'-'+month+'-'+day+'.txt'
    print("We are looking at file: ",file)

    return file


if __name__ == "__main__":
    date_to_text("12/5/2010")
    
    