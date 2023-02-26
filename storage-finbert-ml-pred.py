from google.cloud import storage
import datetime as dt 
import pandas as pd
import io
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification 
import torch

def analyze_sentiment(data, context):

  t2=(dt.datetime.now() - dt.timedelta(days=0))
  current_date=t2.strftime('%Y-%m-%d')
  # Récupération du bucket
  storage_client = storage.Client()
  bucket = storage_client.bucket('data_tweet')
  # Récupération de l'objet blob qui contient les tweets
  file_obj = bucket.blob('daily_tweet/tweets du ' + current_date + '.csv')
  # Télécharger le contenu du fichier en tant que string
  file_content = file_obj.download_as_string()
  # Convert the bytes object to a file-like object
  file_content = io.StringIO(file_content.decode('utf-8'))
  # Parser le fichier CSV en DataFrame pandas
  df = pd.read_csv(file_content)

  df = df.iloc[:100]

  # Sélectionner la colonne à traiter
  column = df['text']
  # Supprimer la ponctuation de chaque élément de la colonne
  column = column.apply(lambda x: re.sub(r'[^\w]', ' ', x))
  # Remplacer la colonne originale par la colonne modifiée
  df['text'] = column

  # Chargement du modèle de sentiment FinBERT
  model = AutoModelForSequenceClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
  tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

  # Analyse de sentiment pour chaque phrase dans le DataFrame
  for i, row in df.iterrows():
    input_ids = torch.tensor(tokenizer.encode(row['text'], add_special_tokens=True)).unsqueeze(0) 
    labels = model(input_ids)[0]
    sentiment = labels.argmax().item()
    df.loc[i, 'sentiment'] = sentiment

  # Enregistrez le DataFrame au format CSV
  csv_data = df.to_csv(index=False)
  # Nom du fichier CSV à créer
  file_name2 = "predictions/finbert_ML_pred_" + current_date + "_0-100.csv"
  # Création du fichier dans le bucket
  bucket.blob(file_name2).upload_from_string(csv_data)

  return f"Le fichier {file_name2} a été créé dans le bucket {bucket}."