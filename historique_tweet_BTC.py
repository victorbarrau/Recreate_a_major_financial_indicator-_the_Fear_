import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
from google.cloud import storage
import os
import google.oauth2.service_account

#creds = google.oauth2.service_account.Credentials.from_service_account_file('/home/code/clef/clef.json',scopes=['https://www.googleapis.com/auth/cloud-platform'])
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/code/clef/clef.json"

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date.today()
date_list = []

#storage_client = storage.Client(credentials=creds)
storage_client = storage.Client()
bucket_name = "data_tweet"

while start_date <= end_date:
    date_string = "since:{} until:{}".format(start_date, start_date + datetime.timedelta(days=1))
    date_list.append(date_string)
    start_date += datetime.timedelta(days=1)

def write_tweets_to_file(tweets,date):
    
    df = pd.DataFrame(tweets, columns=['Datetime', 'Text','retweet','like','lang'])
    df['date'] = pd.to_datetime(df['Datetime']).dt.strftime('%Y-%m-%d')
    df.drop(['Datetime'], axis=1, inplace=True)
    #drop ligne when lang != en
    df = df[df['lang'] == 'en']
    #df drop datetime
    date_of_df=date[6:16]
    df=df[df['date']==date_of_df]
    print(df.head())
    
    csv_data = df.to_csv(index=False)
    # Nom du fichier CSV à créer
    file_name = "daily_tweet/Bitcoin/" + str(date_of_df)+".csv"
    # Récupération du bucket
    bucket = storage_client.bucket(bucket_name)
    # Création du fichier dans le bucket
    bucket.blob(file_name).upload_from_string(csv_data)
    print(f"{file_name} créé avec succès.")



tweets_list = []
for date in date_list:
    df = pd.DataFrame()
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('bitcoin '+str(date) ).get_items()):
        if i>40:
            break
        tweets_list.append([tweet.date, tweet.rawContent,tweet.retweetCount,tweet.likeCount,tweet.lang])
    write_tweets_to_file(tweets_list,date)        

