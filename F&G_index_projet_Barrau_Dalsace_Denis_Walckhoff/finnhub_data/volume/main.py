import datetime
import pandas as pd
from google.cloud import storage
import io
import json
import numpy as np

client = storage.Client()
bucket = client.get_bucket('finnhub_bucket')
volume_bucket = client.get_bucket('data_volume')

crypto_list=['btc', 'bnb', 'doge', 'eth']

current_date = datetime.datetime.now() 
date=current_date.strftime("%Y%m%d")

for crypto in crypto_list:

    file_name='daily/'+crypto+'/finnhub_api_'+str(date)+'.json'
    blob=bucket.get_blob(file_name)
    content=blob.download_as_string()
    data=json.loads(content)
    df=pd.read_json(data)

    volume_df = pd.DataFrame()
    df_final = pd.DataFrame()
    df_final["date"]=df["t"]

    # Convertir les timestamps en dates Python
    df_final['date'] = pd.to_datetime(df_final['date'], unit='s')

    for i in range(len(df)): 

        df_final.loc[i, "evolution_prix"]=(df["o"].iloc[i]-df["c"].iloc[i])/(df["o"].iloc[i]+df["c"].iloc[i])
        df_final.loc[i, "score_volume"]=((1+df_final.loc[i, "evolution_prix"])*df["v"].iloc[i])/(df["v"].iloc[i])
        min_score_volume=df_final['score_volume'].min()
        max_score_volume=df_final['score_volume'].max()
        df_final.loc[i, "index_volume"]=((df_final.loc[i, "score_volume"]-min_score_volume)*100)/(max_score_volume-min_score_volume)

    df_final.to_csv('volume_'+crypto+'_du_'+str(date)+'.csv', index=False)

    csv_data=df_final.to_csv(index=False)
    file_name_daily_volume="daily/"+crypto+"/volume_"+crypto+"_du_"+str(date)+".csv"
    volume_bucket.blob(file_name_daily_volume).upload_from_string(csv_data)
