import urllib.request
import json
from pandas.io.json import json_normalize
from kiteconnect import KiteConnect
import pandas as pd
import numpy as np


#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

""" Script to save margin for stocks which has margin greater then 5 """
url = "https://api.kite.trade/margins/equity"
response = urllib.request.urlopen(url)
content = response.read()
data = json.loads(content.decode("utf8"))
DF = json_normalize(data)
fd_sliced = DF.loc[:, ["tradingsymbol", "mis_multiplier",]]
fd_sliced = fd_sliced[fd_sliced.mis_multiplier>=5]
fd_sliced.to_csv('Margin.csv')

"""  get dump of all NSE instruments  """
Margin = pd.read_csv('portfolio.csv') 
Margin = Margin["tradingsymbol"].values.tolist() 
#print(Margin)
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
Selected = instrument_df[instrument_df.tradingsymbol.isin(Margin)]
#print(Selected)
Selected.to_csv('Instruments.csv')



