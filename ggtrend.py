
from time import sleep
import pandas as pd
import numpy as np
from pytrends.request import TrendReq




last_value_dict={}
def get_last_24h_trend(keyword_list):
    for keyword in keyword_list :
        pytrend = TrendReq(hl='en', tz=360)
        kw_list = [keyword]
        pytrend.build_payload(kw_list, cat=0, timeframe='now 1-d', gprop='')#yyyy-mm-dd 2020-08-01 date  
        df = pytrend.interest_over_time()
        df = df.drop(labels=['isPartial'],axis='columns') #nous indique si les données sont complètes ou non
        value = df.sum()/len(df)
        last_value_dict[keyword]=value
        sleep(2)
    return last_value_dict

print(get_last_24h_trend(["bitcoin","nft",'etherum']))
