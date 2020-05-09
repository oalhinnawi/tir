'''
Python file that contains 
all our processing for text
'''

import pandas
import sys
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
#For Context Keywords
from rake_nltk import Rake
#For Sentiment Analysis
from textblob import TextBlob

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

day_data_path='../data/days/'

def process_day(day, subreddit):
    text,titles,bodies=get_all_text(day,subreddit)
#    text=get_all_text(day,subreddit)
    
    #number of features
    no_features=1000
    
    #number of topics
    no_topics=20
    
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(text)
    tf_feature_names = tf_vectorizer.get_feature_names()

    # Run LDA
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)


    no_top_words = 10
    display_topics(lda, tf_feature_names, no_top_words)

    '''
    Get the general sentiment of the text
    '''
    
    sentiment=get_general_sentiment(titles,bodies)
    print(sentiment)
    
    
    
    
'''
Function that returns three separate lists

One for the titles, one for bodies, one for cumulative text

Input: day and subreddit

output: titles, bodies, and cumulative text lists

'''    
def get_all_text(day,subreddit):
    debug=True
    
    #Get the year from the day for our pathing
    year=day[0:4]
    if(debug):print("THIS IS OUR YEAR:",year)
    
    
    #Constructing our path to the csv
    post_text_data_path=day_data_path+'post/'+year+'/'+day+'.csv'
    if(debug):print("DATA PATH:",post_text_data_path)
    
    #Get the dataframe from the path
    post_df=pandas.read_csv(post_text_data_path,index_col=None,encoding="UTF-8",names=params)

    sub_df=post_df.loc[post_df['subreddit']==subreddit]
                       
    if(len(sub_df)==0):            
        sub_df=post_df.loc[post_df['subreddit']==subreddit.lower()]
    
    
    titles=sub_df.title.values.tolist()
    bodies=sub_df.body.values.tolist()
    
    print("Got ",subreddit," data for",day)
    
    cum_text=titles+bodies

    #Filter out anything in the cumulative text
    cum_text=list(filter(lambda x: (x!='[removed]'),cum_text))
    cum_text=list(filter(lambda x: (x!='[deleted]'),cum_text))
    cum_text=list(filter(lambda x: (type(x)!=float),cum_text))

    
    #Title Filter
    titles=list(filter(lambda x: (x!='[removed]'),titles))
    titles=list(filter(lambda x: (x!='[deleted]'),titles))
    titles=list(filter(lambda x: (type(x)!=float),titles))

    #bodies Filter
    bodies=list(filter(lambda x: (x!='[removed]'),bodies))
    bodies=list(filter(lambda x: (x!='[deleted]'),bodies))
    bodies=list(filter(lambda x: (type(x)!=float),bodies))

    
    if(len(cum_text)<=0):
        sys.exit()
        
    
    return titles,bodies,cum_text
    
    
'''
Function that takes the bodies list and the titles list
and spits out a dict

Input: two lists

output: dict
'''    
def get_general_sentiment(titles,bodies,comments=[]):


    sent_list={
    "posts": 0,  
    "avg_pos_score_post": 0, 
    "avg_neg_score_post": 0, 
    "total_pos_posts": 0,  
    "total_neg_posts": 0,  
    "avg_polarity_post": 0, 
    "avg_post_length": 0, 
    "avg_title_length": 0, 
    
    "comments": 0, 
    "avg_pos_score_com": 0, 
    "avg_neg_score_com": 0, 
    "total_pos_com": 0, 
    "total_neg_com": 0,  
    "avg_polarity_com": 0, 

    "avg_polarity_overall": 0, 
    "total_pos_overall": 0, 
    "total_neg_overall": 0
    
    }
    
    '''
    title analysis, covers the following:
        posts
        avg_pos_score_post
        avg_neg_score_post
        avg_polarity_score_post
        avg_title_length
    '''
    for title in titles:
        pol=TextBlob(title).polarity

        #Length
        sent_list['avg_title_length']+=len(title)
        

        sent_list['posts']+=1
        #Positive
        if(pol>.20):
            sent_list['avg_pos_score_post']+=pol
            sent_list['avg_polarity_post']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_pos_posts']+=1
            sent_list['total_pos_overall']+=1
        #negative
        elif(pol<-.20):
            sent_list['avg_neg_score_post']+=pol
            sent_list['avg_polarity_post']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_neg_posts']+=1
            sent_list['total_neg_overall']+=1
        else:
            sent_list['avg_polarity_post']+=pol

    '''
    Post body analysis covers
    avg body length
    '''
    for body in bodies:
        pol=TextBlob(body).polarity

        #Length
        sent_list['avg_post_length']+=len(body)
        
        #Positive
        if(pol>.20):
            sent_list['avg_pos_score_post']+=pol
            sent_list['avg_polarity_post']+=pol
            sent_list['avg_polarity_overall']+=pol

        #negative
        elif(pol<-.20):
            sent_list['avg_neg_score_post']+=pol
            sent_list['avg_polarity_post']+=pol
            sent_list['avg_polarity_overall']+=pol

        else:
            sent_list['avg_polarity_post']+=pol      


    '''
    Comment body analysis; covers:
        
    '''
    for comment in comments:
        pol=TextBlob(comment).polarity
        sent_list['comments']+=1
        #Positive
        if(pol>.20):
            sent_list['avg_pos_score_comment']+=pol
            sent_list['avg_polarity_comment']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_pos_comment']+=1
            sent_list['total_pos_overall']+=1


        #negative
        elif(pol<-.20):
            sent_list['avg_neg_score_comment']+=pol
            sent_list['avg_polarity_comment']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_neg_comment']+=1
            sent_list['total_neg_overall']+=1

        else:
            sent_list['avg_polarity_post']+=pol    
        

    if(sent_list['comments']>0):
        sent_list['avg_pos_score_post']=sent_list['avg_pos_score_post']/sent_list['posts']
        sent_list['avg_neg_score_post']=sent_list['avg_pos_score_post']/sent_list['posts']
        sent_list['avg_polarity_post']=sent_list['avg_polarity_post']/sent_list['posts']
        sent_list['avg_post_length']=sent_list['avg_post_length']/sent_list['posts']
    
    if(sent_list['comments']>0):
        sent_list['avg_pos_score_comment']=sent_list['avg_pos_score_comment']/sent_list['comments']
        sent_list['avg_neg_score_comment']=sent_list['avg_neg_score_comment']/sent_list['comments']
        sent_list['avg_polarity_comment']=sent_list['avg_polarity_comment']/sent_list['comments']
    return sent_list    
    
'''
Function that takes in the cumulative text and 
spits out the context keywords

Input: Cumulative text array
output: array of context keywords
'''
def get_context_keywords(cumulative_text):
    
    r=Rake()
    
    context_keywords_list=[]
    
    for text in cumulative_text:
        
        keywords=r.get_ranked_phrases(text)
        context_keywords_list.append(keywords)
        
    print(context_keywords_list)
    

def display_topics(model, feature_names, no_top_words):

    topics_list=[]
    
    for topic_idx, topic in enumerate(model.components_):
#        print(topic)
#        sys.exit()

#        print("Topic %d:" % (topic_idx))
#        message+=("Topic %d:" % (topic_idx))
        topics=" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
        topics_list.append(topics)
    print(topics_list)
#        print(message)
if __name__=="__main__":
    process_day('2017-01-01','2007scape')