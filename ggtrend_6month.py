import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from google.cloud import storage
import datetime

def daily_ggtrends(request):
    keyword_list=["bitcoin","nft",'etherum','Dogecoin','BNB']
    now = datetime.datetime.now()
    six_months_ago = (now - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
    for keyword in keyword_list :
        pytrend = TrendReq(hl='en', tz=360)
        kw_list = [keyword]
        pytrend.build_payload(kw_list, cat=0, timeframe=six_months_ago + ' ' + now.strftime('%Y-%m-%d'), gprop='')
        df = pytrend.interest_over_time()
        df = df.drop(labels=['isPartial'],axis='columns') #nous indique si les données sont complètes ou non
        df.reset_index(inplace=True)
        df.rename(columns={"date": "date", keyword: "value"}, inplace=True)
        csv_data = df.to_csv(index=False)
        csv_data = csv_data.encode("utf-8")
        client = storage.Client()
        bucket_name ="data_ggtrends"

        now = datetime.datetime.now()
        current_date=now.strftime("%Y%m%d")
        bucket = client.bucket(bucket_name)
        file_name = keyword+"/6month_trends/6month_trends_"+ current_date +".csv"
        bucket.blob(file_name).upload_from_string(csv_data)
    return f"Le fichier {file_name} a été créé dans le bucket {bucket_name}."
