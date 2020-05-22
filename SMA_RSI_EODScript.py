import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import functions as fn
import Connection as con
from datetime import datetime 
import time

cursor = con.sqlit.cursor()
upward_sma_dir = 'False'
downward_sma_dir = 'False'

Endtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))+" " +"03:15:00"
#Endtime = datetime.strptime(Endtime, '%Y-%m-%d %H:%M:%S')
def trade_signal(df):
    "function to generate signal"
    global upward_sma_dir
    global downward_sma_dir
    for i in range(len(df)):  
        upward_sma_dir = 'False'
        downward_sma_dir = 'False'
        if df["5EMA"].iloc[i] > df['10EMA'].iloc[i] and df["5EMA"].iloc[i-1] < df['10EMA'].iloc[i-1]  and df["RSI"].iloc[i]>55 :
            upward_sma_dir = 'True'
            downward_sma_dir = 'False'
        if df["5EMA"].iloc[i] < df['10EMA'].iloc[i] and df["5EMA"].iloc[i-1] > df['10EMA'].iloc[i-1] and df["RSI"].iloc[i]<47.5:
            upward_sma_dir= 'False'
            downward_sma_dir = 'True'  
        if upward_sma_dir == 'True':
            DF["signal"].iloc[i] = "Buy"
        if downward_sma_dir == 'True':
            DF["signal"].iloc[i] = "Sell"
    #return signal
    return df
DF = fn.fetchOHLC('HDFC',5)
DF["5EMA"]=round(DF["close"].ewm(span=5,min_periods=5).mean(),2)
DF["10EMA"]=round(DF["close"].ewm(span=10,min_periods=10).mean(),2)
DF=fn.RSI(DF,14)
DF["signal"] = ''
DF=trade_signal(DF)
qry1 = "Delete from OHLC_TICKER"
qry2 = "Delete from PORTFOLIO where date >'" +Endtime+"'"
#print(qry2)
cursor.execute(qry1)
cursor.execute(qry2)
con.sqlit.commit()
for i in range(len(DF)):
    qry = "insert into OHLC_TICKER(Date,instrument_token,OPEN,CLOSE,HIGH,LOW,EMA5,EMA10,RSI,SIGNAL) values(?,?,?,?,?,?,?,?,?,?);"
    cursor.execute(qry ,(datetime.strptime(str(DF.index[i]),'%Y-%m-%d %H:%M:%S'),int(DF["instrument_token"].iloc[i]),DF["open"].iloc[i],DF["high"].iloc[i],DF["low"].iloc[i] ,DF["close"].iloc[i] ,DF["5EMA"].iloc[i] ,DF["10EMA"].iloc[i],DF["RSI"].iloc[i],DF["signal"].iloc[i]))
    con.sqlit.commit()
con.sqlit.close()