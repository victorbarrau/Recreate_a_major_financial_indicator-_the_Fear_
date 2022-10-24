#import google trend data 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq

def plot_searchterms(df):
    """Plots google trends
    
    Parameters
    ----------
    df: pandas dataframe
        As returned from pytrends, without the "isPartial" column
    
    Returns
    -------
    ax: axis handle
    """
    fig = plt.figure(figsize = (15,8))
    ax = fig.add_subplot(111)
    df.plot(ax=ax)
    plt.ylabel('Relative search term frequency')
    plt.xlabel('Date')
    plt.ylim((0,120))
    plt.legend(loc='lower left')
    
    return ax

pytrend = TrendReq(hl='en', tz=360)
kw_list = ["bitcoin","dash","Nft","crypto","blockchain"]
pytrend.build_payload(kw_list, cat=0, timeframe='today', geo='', gprop='')#yyyy-mm-dd 2020-08-01 date  
df = pytrend.interest_over_time()
df = df.drop(labels=['isPartial'],axis='columns') #nous indique si les données sont complètes ou non
plot_searchterms(df)