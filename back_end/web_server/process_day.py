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
#For wordcloud visualizations
from wordcloud import WordCloud
#For making the final FPDF
from fpdf import FPDF
import os

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
    titles,bodies,comments,text=get_all_text(day,subreddit)
#    text=get_all_text(day,subreddit)
    '''
    Topics analysis
    '''
    print("Getting the topics")
    #number of features
    no_features=1000
    
    #number of topics
    no_topics=100
    
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(text)
    tf_feature_names = tf_vectorizer.get_feature_names()

    # Run LDA
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)


    no_top_words = 20
    topics_list=display_topics(lda, tf_feature_names, no_top_words)

    '''
    Context Keywords
    '''
    print("Getting Context Keywords")

    context_keywords=get_context_keywords(text)

    '''
    Get the general sentiment of the text
    '''

    print("Getting General Sentiment")

    sentiment=get_general_sentiment(titles,bodies,comments)
    print(sentiment)


    '''
    Get the visualizations
    '''
    create_visualizations(topics_list,sentiment,context_keywords)

    '''
    Create the PDF
    '''
    create_pdf()

    print("All processes done, sending to web server")
    return topics_list,sentiment,context_keywords
    
'''
Function that creates pdf form the generated images from our analysis
'''
def create_pdf():
    pdf=FPDF()
    image_list=['topic_img.png','sent_img.png','ck_img.png']
    pdf.add_page()
    pdf.image('images/topic_img.png',15,0,120,80)
    pdf.image('images/sent_img.png',15,80,140,80)
    pdf.image('images/ck_img.png',15,160,130,80)
    pdf.output("Analysis.pdf","F")
    pdf.close()
'''
Function that creates visualizations for each of the thingies
'''
def create_visualizations(topics_list,sentiment,context_keywords):
    '''
    Create the visualization for the sentiment analysis
    '''
    print("Creating Graph for sentiment")
    sent_data=pandas.DataFrame.from_dict(sentiment,orient='index')
    sent_ax=sent_data.plot.barh(title="Sentiment Analysis")
    for p in sent_ax.patches:
        sent_ax.annotate("%.2f" % p.get_width(), (p.get_x() + p.get_width()+0.5, p.get_y()-0.8), xytext=(0, 10), textcoords='offset points')
    sent_img=sent_ax.get_figure()
    sent_img.savefig("images/sent_img.png",bbox_inches='tight')
    '''
    Create a visualizations for the context keywords
    '''
    print("Creating Visualization for the context keywords")
    ck_dict={}
    for sentence in context_keywords:
        for arr in sentence:
            for word in arr.split():
                if word in ck_dict:
                    ck_dict[word]+=1
                else:
                    ck_dict[word]=1      
    ck_data=pandas.DataFrame.from_dict(ck_dict,orient='index',columns=['frequency'])
    ck_data=ck_data.sort_values(by='frequency',ascending=False)    
    ck_data=ck_data.head(10)
    ck_ax=ck_data.plot.barh(color=['c','y'],title="Context Keywords")
    for p in ck_ax.patches:
        ck_ax.annotate("%.2f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()-0.5), xytext=(0, 10), textcoords='offset points')    
    ck_img=ck_ax.get_figure()
    ck_img.savefig("images/ck_img.png",bbox_inches='tight')
    '''
    Create a visualization for the topics
    '''
    print("Creating Wordcloud for topics")
    topic_dict={}
    for arr in topics_list:
        for word in arr.split():
            if word in topic_dict:
                topic_dict[word]+=1
            else:
                topic_dict[word]=1   
    topic_data=pandas.DataFrame.from_dict(topic_dict,orient='index',columns=['confidence'])
    topic_data=topic_data.sort_values(by='confidence',ascending=False)
    topic_data=topic_data.head(10)
    topic_ax=topic_data.plot.barh(color=['r','c'],title="Topic confidence")
    for p in topic_ax.patches:
        topic_ax.annotate("%.2f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()-0.5), xytext=(0, 10), textcoords='offset points')
    topic_img=topic_ax.get_figure()
    topic_img.savefig("images/topic_img.png",bbox_inches='tight')
    
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
    comment_text_data_path=day_data_path+'comment/'+year+'/'+day+'.csv'
    if(debug):print("DATA PATH:",post_text_data_path)
    
    #Get the dataframe from the path
    post_df=pandas.read_csv(post_text_data_path,index_col=None,encoding="UTF-8",names=params)

    comment_df=pandas.read_csv(comment_text_data_path,index_col=None,encoding="UTF-8",names=params)

    comment_df=comment_df.loc[comment_df['subreddit']==subreddit]

    sub_df=post_df.loc[post_df['subreddit']==subreddit]
                       
    if(len(sub_df)==0):            
        sub_df=post_df.loc[post_df['subreddit']==subreddit.lower()]
    
    
    titles=sub_df.title.values.tolist()
    bodies=sub_df.body.values.tolist()
    comments=comment_df.body.values.tolist()
    print("Got ",subreddit," data for",day)
    
    cum_text=titles+bodies+comments

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

    #comments filter
    comments=list(filter(lambda x: (x!='[removed]'),comments))
    comments=list(filter(lambda x: (x!='[deleted]'),comments))
    comments=list(filter(lambda x: (type(x)!=float),comments))
    
    
    if(len(cum_text)<=0):
        sys.exit()
        
    
    return titles,bodies,comments,cum_text
    
    
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
            sent_list['avg_pos_score_com']+=pol
            sent_list['avg_polarity_com']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_pos_com']+=1
            sent_list['total_pos_overall']+=1


        #negative
        elif(pol<-.20):
            sent_list['avg_neg_score_com']+=pol
            sent_list['avg_polarity_com']+=pol
            sent_list['avg_polarity_overall']+=pol
            sent_list['total_neg_com']+=1
            sent_list['total_neg_overall']+=1

        else:
            sent_list['avg_polarity_post']+=pol    
        

    if(sent_list['posts']>0):
        sent_list['avg_pos_score_post']=sent_list['avg_pos_score_post']/sent_list['posts']
        sent_list['avg_neg_score_post']=sent_list['avg_neg_score_post']/sent_list['posts']
        sent_list['avg_polarity_post']=sent_list['avg_polarity_post']/sent_list['posts']
        sent_list['avg_post_length']=sent_list['avg_post_length']/sent_list['posts']
        sent_list['avg_title_length']=sent_list['avg_title_length']/sent_list['posts']
    
    if(sent_list['comments']>0):
        sent_list['avg_pos_score_com']=sent_list['avg_pos_score_com']/sent_list['comments']
        sent_list['avg_neg_score_com']=sent_list['avg_neg_score_com']/sent_list['comments']
        sent_list['avg_polarity_com']=sent_list['avg_polarity_com']/sent_list['comments']
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
        
        r.extract_keywords_from_text(text)
        
        keywords=r.get_ranked_phrases()
        
        context_keywords_list.append(keywords)
        
    return(context_keywords_list)
    

def display_topics(model, feature_names, no_top_words):

    topics_list=[]
    
    for topic_idx, topic in enumerate(model.components_):
#        print(topic)
#        sys.exit()

#        print("Topic %d:" % (topic_idx))
#        message+=("Topic %d:" % (topic_idx))
        topics=" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
        topics_list.append(topics)

    return(topics_list)
    

if __name__=="__main__":
    topics_list,sentiment,context_keywords=process_day('2017-01-01','AskMen')
