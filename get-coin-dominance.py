import requests
import json
import time
import datetime as dt
import pandas as pd
from google.cloud import storage

#fonction qui récupère les données de l'api CoinMarketCAp et les stock dans un json
def get_market_dominance(request):
  #timestamp
  t2=(dt.datetime.now())
  #unix timestamp
  unix_t2=int(time.mktime(t2.timetuple()))
  #get data
  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
  parameters = {
    "convert": "USD"
  }
  headers = {
    "Accepts": "application/json",
    "X-CMC_Pro_API_Key": ""
  }
  response = requests.get(url, headers=headers, params=parameters)

  data = response.json()
  current_date=t2.strftime("%Y%m%d")

  #BTC
  btc_data = json.loads(response.text)['data'][0]["quote"]
  df_btc=pd.DataFrame.from_dict(btc_data)
  df_btc=df_btc.iloc[3,]
  json_btc={
    'symbol':['BTC'],
    'dominance':[str(df_btc["USD"])]
  }
  df=pd.DataFrame(json_btc)
  btc_csv=df.to_csv(index=False)
  # Instanciation de l'objet Storage
  storage_client = storage.Client()
  # Nom du bucket Cloud Storage
  bucket_name = "data-coin-market-cap"
  # Nom du fichier JSON à créer 
  file_name1 = "btc/daily/dominance_du_" + current_date + ".csv"
  # Récupération du bucket
  bucket = storage_client.bucket(bucket_name)
  # Création du fichier dans le bucket
  bucket.blob(file_name1).upload_from_string(btc_csv)


  #ETH
  eth_data = json.loads(response.text)['data'][1]["quote"]
  df_eth=pd.DataFrame.from_dict(eth_data)
  df_eth=df_eth.iloc[3,]
  json_eth={
    'symbol':['ETH'],
    'dominance':[str(df_eth["USD"])]
  }
  df2=pd.DataFrame(json_eth)
  eth_csv=df2.to_csv(index=False)
  # Nom du fichier JSON à créer
  file_name2 = "eth/daily/dominance_du_" + current_date + ".csv"
  # Création du fichier dans le bucket
  bucket.blob(file_name2).upload_from_string(eth_csv)


  #BNB
  bnb_data = json.loads(response.text)['data'][3]["quote"]
  df_bnb=pd.DataFrame.from_dict(bnb_data)
  df_bnb=df_bnb.iloc[3,]
  json_bnb={
    'symbol':['BNB'],
    'dominance':[str(df_bnb["USD"])]
  }
  df3=pd.DataFrame(json_bnb)
  bnb_csv=df3.to_csv(index=False)
  # Nom du fichier JSON à créer
  file_name3 = "bnb/daily/dominance_du_" + current_date + ".csv"
  # Création du fichier dans le bucket
  bucket.blob(file_name3).upload_from_string(bnb_csv)


  #DOGE
  doge_data = json.loads(response.text)['data'][8]["quote"]
  df_doge=pd.DataFrame.from_dict(doge_data)
  df_doge=df_doge.iloc[3,]
  json_doge={
    'symbol':['DOGE'],
    'dominance':[str(df_doge["USD"])]
  }
  df4=pd.DataFrame(json_doge)
  doge_csv=df4.to_csv(index=False)
  #store data in a json
  json_object4 = json.dumps(doge_data, indent = 4)
  json_data4 = json.dumps(json_object4).encode("utf-8")
  # Nom du fichier JSON à créer
  file_name4 = "doge/daily/dominance_du_" + current_date + ".csv"
  # Création du fichier dans le bucket
  bucket.blob(file_name4).upload_from_string(doge_csv)

  return f"Les fichiers ont été créé dans le bucket {bucket_name}."
