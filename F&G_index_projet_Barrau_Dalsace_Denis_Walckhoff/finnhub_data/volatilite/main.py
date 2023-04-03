import datetime 
import pandas as pd
from google.cloud import storage
import io
import re
import json
import numpy as np

def volatility(data, context):
    crypto_list=['bnb', 'btc', 'doge', 'eth']
    current_date = datetime.datetime.now() 
    yesterday_date = current_date - datetime.timedelta(days=1)
    date=current_date.strftime("%Y%m%d")
    date_yest=yesterday_date.strftime("%Y%m%d")
    date_generated = [date.strftime("%Y%m%d") for date in [current_date + datetime.timedelta(days=x) for x in range((yesterday_date-current_date).days+1)]]

    client = storage.Client()
    bucket=client.get_bucket('finnhub_bucket')
    volat_bucket=client.get_bucket('data_volatility')
    
    for crypto in crypto_list:

        #df_hist=pd.read_csv("histo_finnhub/history_finnhub_"+crypto+".csv")

        file_name='daily/'+crypto+'/finnhub_api_'+str(date)+'.json'
        blob=bucket.get_blob(file_name)
        content=blob.download_as_string()
        data=json.loads(content)
        df=pd.read_json(data)

        file_name_hist="tmp/history_finnhub_"+crypto+".csv"
        blob1=volat_bucket.get_blob(file_name_hist)
        content1=blob1.download_as_string()
        df_hist=pd.read_csv(io.StringIO(content1.decode('utf-8')))

        # Concaténer les DataFrames verticalement
        df_concat = pd.concat([df_hist, df]) 
        df_concat.reset_index(drop=True, inplace=True) # Utiliser drop=True pour supprimer la colonne d'index précédente
        print(df_concat)
        csv_tmp=df_concat.to_csv(index=False)
        file_name_tmp="tmp/history_finnhub_"+crypto+".csv"
        volat_bucket.blob1(file_name_tmp).upload_from_string(csv_tmp)

        volat_df = pd.DataFrame()
        df_final = pd.DataFrame()
        df_final["date"]=df_concat["t"]
        for i in range(len(df_concat)):
            df_final.loc[i, "volatilite"] = abs(((df_concat["o"].iloc[i]-df_concat["c"].iloc[i]))) # prix d'ouverture du jour - prix ouverture hist = volat daily
            df_final.loc[i, "historical_volatility"]=(df_final["volatilite"].mean())
            df_final.loc[i, "score"]=(abs(df_final.loc[i, "historical_volatility"]-df_final.loc[i, "volatilite"]))/(abs(df_final.loc[i, "historical_volatility"]+df_final.loc[i, "volatilite"]))

        df_final=df_final[::-1]
        df_final=df_final.iloc[0:1,:] 
        
        csv_data=df_final.to_csv(index=False)
        file_name_daily_volatility="daily/"+crypto+"/volatilite_"+crypto+"_du_"+date+".csv"
        volat_bucket.blob(file_name_daily_volatility).upload_from_string(csv_data)
