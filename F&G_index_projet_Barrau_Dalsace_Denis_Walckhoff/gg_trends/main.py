import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from google.cloud import storage
import datetime


def daily_ggtrends(request):
    keyword_list=["bitcoin","nft",'etherum','Dogecoin','BNB']
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    bucket_name ="data_ggtrends"
    for keyword in keyword_list :
        pytrend = TrendReq(hl='en', tz=360)
        kw_list = [keyword]

        pytrend.build_payload(kw_list, cat=0,timeframe='now 1-d', gprop='')
        df = pytrend.interest_over_time()
        df = df.drop(labels=['isPartial'],axis='columns') #nous indique si les données sont complètes ou non
        df.reset_index(inplace=False)
        df.rename(columns={"date": "date", keyword: "value"}, inplace=True)
        last_value_dict={}
        value = df.sum()/len(df)
        last_value_dict[keyword]=value[0]
        last_value_dict['date']=today
        index=[0]
        df = pd.DataFrame(last_value_dict,index=index)
        csv_data = df.to_csv(index=True)
        #save the csv local file

        csv_data = csv_data.encode("utf-8")
        client = storage.Client()

        now = datetime.datetime.now()
        current_date=now.strftime("%Y%m%d")
        bucket = client.bucket(bucket_name)
        file_name = keyword+"/daily_trends/trends_"+ current_date +".csv"

        bucket.blob(file_name).upload_from_string(csv_data)    
    return f"Le fichier {file_name} a été créé dans le bucket {bucket_name}."