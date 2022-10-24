
#import google trend data 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq
pytrend = TrendReq(hl='en-US', tz=360)
kw_list = ["Bitcoin"]
pytrend.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
df = pytrend.interest_over_time()
df = df.drop(labels=['isPartial'],axis='columns')
df.plot()
plt.show()