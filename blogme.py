# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:51:42 2022

@author: sankalp
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# reading xlsx files
data = pd.read_excel('articles.xlsx')

# summary of data
data.describe()

# summary of columns
data.info()

# counting the number of articles per source
# format of groupby: df.groupby(['column_to_group'])['column_to_count'].count()
data.groupby(['source_id'])['article_id'].count()

# number of reactions per publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

# dropping column
data = data.drop('engagement_comment_plugin_count', axis=1)     # axis = 1 (column)


# creating function
# deal with 'nan' we need to make use of try and except

def keywordflag(keyword):
    keyword_flag = []
    length = len(data)
    for x in range(0, length):
        heading = data['title'][x]
        try:
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except:             # if you encounter float, nan etc.
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

# creating a flag word
keyword_flag = keywordflag('murder')

# creating a new column
data['keyword_flag'] = pd.Series(keyword_flag)

# SentimentIntensityAnalyzer - on title
# adding a for loop to extract sentiment per title
title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

length = len(data)

for x in range(0, length):
    try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)
    
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)

data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment

# writing back to excel file
data.to_excel('blogme_cleaned.xlsx', sheet_name = 'blogmedata', index=False)