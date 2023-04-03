import requests
import json
import time
import datetime as dt
import pandas as pd
from google.cloud import storage
import io
import numpy as np

#fonction qui récupère les données de l'api CoinMarketCAp et les stock dans un json
def get_market_dominance(request):
  #timestamp
  t2=(dt.datetime.now())
  current_date2=t2.strftime("%Y-%m-%d")
  #unix timestamp
  unix_t2=int(time.mktime(t2.timetuple()))
  #get data
  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
  parameters = {
    "convert": "USD"
  }
  headers = {
    "Accepts": "application/json",
    "X-CMC_Pro_API_Key": "c0c3de3e-77cd-4aac-87f1-f3e5f7d645b6"
  }
  response = requests.get(url, headers=headers, params=parameters)

  data = response.json()
  current_date=t2.strftime("%Y%m%d")

  #BTC
  btc_data = json.loads(response.text)['data'][0]["quote"]
  df_btc=pd.DataFrame.from_dict(btc_data)
  df_btc=df_btc.iloc[3,]
  json_btc={
    'date':[str(current_date2)],
    'dominance':[str(df_btc["USD"])]
  }
  df=pd.DataFrame(json_btc)

  client = storage.Client()
  bucket = client.get_bucket('data-coin-market-cap')
  file_name_hist='btc/tmp/dominance_historique_btc.csv'
  blob=bucket.get_blob(file_name_hist)
  content=blob.download_as_string()
  df_hist=pd.read_csv(io.StringIO(content.decode('utf-8')))

  df_concat = pd.DataFrame()
  df_concat = pd.concat([df_hist, df]) 
  df_concat.reset_index(drop=True, inplace=True)
  df_concat["dominance"]= pd.to_numeric(df_concat['dominance'], errors='coerce').astype(float)

  for i in range(len(df_concat)): 

      min_score_dominance=df_concat['dominance'].min()
      max_score_dominance=df_concat['dominance'].max()
      # 1 - (max - daily / max - min)
      df_concat.loc[i, "score_dominance"]=1-abs((max_score_dominance-df_concat.loc[i, "dominance"])/(max_score_dominance-min_score_dominance))
      df_concat["score_dominance"]= pd.to_numeric(df_concat['score_dominance'], errors='coerce').astype(float)

  df_final = pd.DataFrame()
  df_final=df_concat 
  df_final=df_final[::-1]
  df_final=df_final.iloc[0:1,:] 

  btc_csv=df_final.to_csv(index=False)
  storage_client = storage.Client()
  bucket_name = "data-coin-market-cap"
  file_name1 = "btc/daily/dominance_btc_du_" + current_date + ".csv"
  bucket = storage_client.bucket(bucket_name)
  bucket.blob(file_name1).upload_from_string(btc_csv) 

  tmp_csv=df_concat.to_csv(index=False)
  file_name2 = "btc/tmp/dominance_historique_btc.csv"
  bucket.blob(file_name2).upload_from_string(tmp_csv) 


  return f"Les fichiers ont été créé dans le bucket {bucket_name}."
