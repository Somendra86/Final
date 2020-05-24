""" 
EMA CrossOver with RSI
@author: Somendra Chaudhary
"""
from kiteconnect import KiteConnect
import os
import datetime as dt
import pandas as pd
import time
import sys
import functions as fn
import Connection as con
from datetime import datetime 
import datetime
global tickers
cursor = con.sqlit.cursor()

Instruments = pd.read_csv('portfolio.csv') 
tickers  = Instruments["tradingsymbol"].values.tolist()
interval = 5
capitalPerStock = 20000
executed = []
cwd = os.chdir("F:/Final")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

def main():
    global capitalPerStock
    a,b = 0,0
    while a < 10:
        try:
            pos_df = pd.DataFrame(kite.positions()["day"])
            break
        except:
            print("can't extract position data..retrying")
            a+=1
    while b < 10:
        try:
            ord_df = pd.DataFrame(kite.orders())
            break
        except:
            print("can't extract order data..retrying")
            b+=1
    for ticker in tickers:
        print("starting passthrough for....."+ticker)
        try:
            ohlc = fn.fetchOHLC(ticker,interval)
            signal=fn.EmaCrossOver(ohlc)
            print("Signal "+ signal + " raise at -"+ str(ohlc.index[-1]))
            # if len(pos_df.columns)==0:
            #     if signal =="Buy":
            #         executed.append(ticker)
            #         quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #         atr = atr(ohlc,14)
            #         fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2])
            #     if signal =="Sell": 
            #         executed.append(ticker) 
            #         quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #         atr = atr(ohlc,14)
            #         fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2]) 

            # if len(pos_df.columns)!=0 and ticker not in pos_df["tradingsymbol"].tolist():
            #     if signal =="Buy":
            #         executed.append(ticker)
            #         quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #         atr = atr(ohlc,14)
            #         fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2])
            #     if signal =="Sell": 
            #         executed.append(ticker) 
            #         quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #         atr = atr(ohlc,14)
            #         fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2]) 

            #  if len(pos_df.columns)!=0 and ticker in pos_df["tradingsymbol"].tolist():  
            #      if pos_df[pos_df["tradingsymbol"]==ticker]["quantity"].values[0] == 0:
            #          if signal =="Buy":
            #             executed.append(ticker)
            #             quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #             atr = atr(ohlc,14)
            #             fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2])
            #         if signal =="Sell": 
            #             executed.append(ticker) 
            #             quantity=fn.tradeQuantity(ticker,capitalPerStock,ohlc["close"][-2])
            #             atr = atr(ohlc,14)
            #             fn.placeBracketOrder(ticker,signal,quantity,atr,ohlc["close"][-2]) 
                     
        except Exception as e:
            print("API error for ticker :",ticker)
            print("Signal functon failed at -"+ str(ohlc.index[-1]) +" - "+ e)

while True:
    now = datetime.datetime.now()
    isholiday = fn.isholiday(now)
    if (now.hour >= 9 and now.minute >= 15 and not now.weekday() in (5,6) and isholiday=="False"):
        try:
            print("passthrough at " +time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            main()
            time.sleep(5)
        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')
            exit()
    if (not now.weekday() in (5,6) and isholiday == "False"):    
        if (now.hour >= 15 and now.minute >= 29 ):        
            sys.exit()  
    else:
        print("Weekend or Holiday")    
        sys.exit()                 
exit()
