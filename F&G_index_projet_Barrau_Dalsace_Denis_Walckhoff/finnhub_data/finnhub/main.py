import finnhub
import json
import time
import datetime as dt
from google.cloud import storage
import datetime
import pandas as pd
from google.cloud import storage
import os
import io
import re
import google.oauth2.service_account
import json
import numpy as np

creds = google.oauth2.service_account.Credentials.from_service_account_file('./clef.json',scopes=['https://www.googleapis.com/auth/cloud-platform'])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./clef.json"
client = storage.Client(credentials=creds)
bucket = client.get_bucket('finnhub_bucket')

#fonction qui récupère les données de historique l'api finnhub et les stock dans un json
def get_finnhub_data_history(request):
  #get history data
  finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")

  dict_crypto=finnhub_client.crypto_candles('BINANCE:DOGEUSDT', 'D', 1609459200, 1679356800)
  #store data in a json
  json_object = json.dumps(dict_crypto, indent = 4)
  json_data = json.dumps(json_object).encode("utf-8")
  # Instanciation de l'objet Storage
  storage_client = storage.Client()
  # Nom du bucket Cloud Storage
  bucket_name = "finnhub_bucket"
  # Nom du fichier JSON à créer
  file_name = "history/doge/finnhub_api_history.json"
  # Récupération du bucket
  bucket = storage_client.bucket(bucket_name)
  # Création du fichier dans le bucket
  bucket.blob(file_name).upload_from_string(json_data)

#   dict_crypto2=finnhub_client.crypto_candles('BINANCE:ETHUSDT', 'D', 1609459200, 1679356800)
#   #store data in a json
#   json_object2 = json.dumps(dict_crypto2, indent = 4)
#   json_data2 = json.dumps(json_object2).encode("utf-8")
#   # Nom du fichier JSON à créer
#   file_name2 = "history/eth/finnhub_api_history.json"
#   # Création du fichier dans le bucket
#   bucket.blob(file_name2).upload_from_string(json_data2)

#   dict_crypto3=finnhub_client.crypto_candles('BINANCE:BNBUSDT', 'D', 1609459200, 1679356800)
#   #store data in a json
#   json_object3 = json.dumps(dict_crypto3, indent = 4)
#   json_data3 = json.dumps(json_object3).encode("utf-8")
#   # Nom du fichier JSON à créer
#   file_name3 = "history/bnb/finnhub_api_history.json"
#   # Création du fichier dans le bucket
#   bucket.blob(file_name3).upload_from_string(json_data3)

#   dict_crypto4=finnhub_client.crypto_candles('BINANCE:DOGEUSDT', 'D', 1609459200, 1679356800)
#   #store data in a json
#   json_object4 = json.dumps(dict_crypto4, indent = 4)
#   json_data4 = json.dumps(json_object4).encode("utf-8")
#   # Nom du fichier JSON à créer
#   file_name4 = "history/doge/finnhub_api_history.json"
#   # Création du fichier dans le bucket
#   bucket.blob(file_name4).upload_from_string(json_data4)

  return f"Le fichier {file_name} a été créé dans le bucket {bucket_name}."
get_finnhub_data_history(1)