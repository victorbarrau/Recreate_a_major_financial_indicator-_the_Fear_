
import os
import tweepy as tw
import pandas as pd
from tweepy import OAuth1UserHandler, API
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from datetime import date
from datetime import datetime, timedelta
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

#Put your Bearer Token in the parenthesis below
client = tw.Client(bearer_token='')

# ne fonctionne plus avec les dates : query = 'BTC -is:retweet lang:en since:{} until:{}'.format(date_since,date_now)
#-is:retweet = ne pas prendre les retweet
query = 'BTC -is:retweet lang:en'
tweets = tw.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)
tweets_copy=tweets
X=[]
publication_time=[] 
i=0
for tweet in tweets:
    shifted = tweet.id >> 22 
    timestamp = shifted + 1288834974657
    time_created = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
    publication_time.append(time_created)
    X.append(tweet.text)
    i+=1
print(i)

df=pd.DataFrame()
df['text']=X
df['date']=publication_time

print(df)

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

nlp=pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

results = nlp(df['text'][:100,].to_list())
print(results)




