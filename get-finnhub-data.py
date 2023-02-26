import finnhub
import json
import time
import datetime as dt
from google.cloud import storage

#fonction qui récupère les données de l'api finnhub et les stock dans un json
def get_finnhub_data_daily(request):
  #timestamp 
  t1=(dt.datetime.now() - dt.timedelta(days=1))
  t2=(dt.datetime.now())
  #unix timestamp
  unix_t1=int(time.mktime(t1.timetuple()))
  unix_t2=int(time.mktime(t2.timetuple()))
  #get data
  finnhub_client = finnhub.Client(api_key="")
  current_date=t2.strftime("%Y%m%d")

  #BTC
  dict_crypto1=finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', unix_t1, unix_t2)
  #store data in a json
  json_object1 = json.dumps(dict_crypto1, indent = 4)
  json_data1 = json.dumps(json_object1).encode("utf-8")
  # Instanciation de l'objet Storage
  storage_client = storage.Client()
  # Nom du bucket Cloud Storage
  bucket_name = "finnhub_bucket"
  # Nom du fichier JSON à créer
  file_name1 = "daily/btc/finnhub_api_" + current_date + ".json"
  # Récupération du bucket
  bucket = storage_client.bucket(bucket_name)
  # Création du fichier dans le bucket
  bucket.blob(file_name1).upload_from_string(json_data1)

  #BNB
  dict_crypto2=finnhub_client.crypto_candles('BINANCE:BNBUSDT', 'D', unix_t1, unix_t2)
  #store data in a json
  json_object2 = json.dumps(dict_crypto2, indent = 4)
  json_data2 = json.dumps(json_object2).encode("utf-8")
  # Nom du fichier JSON à créer
  file_name2 = "daily/bnb/finnhub_api_" + current_date + ".json"
  # Création du fichier dans le bucket
  bucket.blob(file_name2).upload_from_string(json_data2)

  #DOGE
  dict_crypto3=finnhub_client.crypto_candles('BINANCE:DOGEUSDT', 'D', unix_t1, unix_t2)
  #store data in a json
  json_object3 = json.dumps(dict_crypto3, indent = 4)
  json_data3 = json.dumps(json_object3).encode("utf-8")
  # Nom du fichier JSON à créer
  file_name3 = "daily/doge/finnhub_api_" + current_date + ".json"
  # Création du fichier dans le bucket
  bucket.blob(file_name3).upload_from_string(json_data3)

  #ETH
  dict_crypto4=finnhub_client.crypto_candles('BINANCE:ETHUSDT', 'D', unix_t1, unix_t2)
  #store data in a json
  json_object4 = json.dumps(dict_crypto4, indent = 4)
  json_data4 = json.dumps(json_object4).encode("utf-8")
  # Nom du fichier JSON à créer
  file_name4 = "daily/eth/finnhub_api_" + current_date + ".json"
  # Création du fichier dans le bucket
  bucket.blob(file_name4).upload_from_string(json_data4)

  return f"Les fichiers ont été créé dans le bucket {bucket_name}."


