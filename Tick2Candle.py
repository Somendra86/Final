from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import os
import time
from datetime import datetime
import functions
import Connection as con
import sys

kws = ""
kite = ""
cwd = os.chdir("C:/Final")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
kws = KiteTicker(key_secret[0],access_token)
portfolio = pd.read_csv('portfolio.csv')
Instruments = pd.read_csv('Instruments.csv') 
subscribe  = Instruments["instrument_token"].values.tolist()
cursor = con.sqlit.cursor()

def on_ticks(ws, ticks):
        for tick in ticks:
            try:
                instrument_token = tick["instrument_token"]
                Date = tick["timestamp"]
                buy_quantity = tick["buy_quantity"]
                sell_quantity = tick["sell_quantity"]
                last_price = tick["last_price"]
                volume = tick["volume"]
                average_price = tick["average_price"]
                qry = "insert into PORTFOLIO(instrument_token,Date,buy_quantity,sell_quantity,last_price,Volume,average_price) values(?,?,?,?,?,?,?);"
                cursor.execute(qry ,(instrument_token,Date,buy_quantity,sell_quantity,last_price,volume,average_price))
            except:
                pass    
        try:    
            con.sqlit.commit()
        except Exception as e:
            con.sqlit.rollback()
            print(e)
                

def on_connect(ws, response):
    ws.subscribe(subscribe)
    ws.set_mode(ws.MODE_FULL, subscribe)
    
# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.connect()

while True:
    now = datetime.datetime.now()
    if (now.hour >= 9 and now.minute >= 15 ):
        kws.on_ticks=on_ticks
        kws.on_connect=on_connect
        kws.connect()
    if (now.hour >= 15 and now.minute >= 29):
        sys.exit()
con.sqlit.close()