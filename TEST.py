from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import os
import time
from datetime import datetime
import datetime
import functions
import Connection as con
import sys

kws = ""
kite = ""
cwd = os.chdir("F:/Final")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
kws = KiteTicker(key_secret[0],access_token)

holdings = pd.DataFrame(kite.holdings())
# print(kite.holdings())
# print(holdings)
# print(holdings['tradingsymbol'] == 'IDEA')

print(holdings.loc[(holdings['tradingsymbol'] == 'IDEA') & (holdings['isin'].isin(["INE669E01016"]))]["instrument_token"])