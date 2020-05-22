import pandas as pd
import datetime as dt
import Connection as con
import numpy as np
from datetime import datetime 
from kiteconnect import KiteConnect

cursor = con.sqlit.cursor()
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

upward_sma_dir = False
downward_sma_dir = False
signal = []
""" get margin for individual stock given by broker"""
def getMargin(ticker):
        try:
            Margin=pd.read_csv("Margin.csv")
            Margin = Margin[Margin.tradingsymbol == ticker]
            return Margin.iloc[0]["mis_multiplier"]
        except:
            print("error encountered while fetching Margin")

# # a=getMargin("HDFC")    
# # print(a)

def getInstrumentNum(ticker):
        try:
            Instrument  = pd.read_csv("Instruments.csv")
            Instrument = Instrument[Instrument.tradingsymbol == ticker]
            return Instrument.iloc[0]["instrument_token"]
        except:
            print("error encountered while fetching Instrument token")

# # a=getInstrumentNum("HDFC") 
# # print(a)

def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta']=df['close'] - df['close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].ewm(com=n,min_periods=n).mean().tolist()[n]) 
            avg_loss.append(df['loss'].ewm(com=n,min_periods=n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = round(100 - (100/(1+df['RS'])),2)
    df = df.drop(columns=['delta','gain','loss','avg_gain','avg_loss','RS'] , axis = 1)
    return df

def fetchOHLC(ticker,interval):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = getInstrumentNum(ticker)
    query = 'SELECT Date,instrument_token,last_price FROM PORTFOLIO where instrument_token = '+str(instrument) +' order by Date'
    df = pd.read_sql(query, con.sqlit , parse_dates = "Date")
    df.set_index("Date",inplace=True)
    ohlc = df["last_price"].resample(str(interval)+'Min').ohlc().dropna(how='any')
    ohlc["last_price"] = df["last_price"].iloc[-1]
    ohlc["instrument_token"] = df["instrument_token"].iloc[-1]
    ohlc["average_price"] = df["average_price"].iloc[-1]
    return ohlc
    #print(df)

# OHLC = fetchOHLC("HDFC",5)
# print(OHLC)

    
def tradeQuantity(ticker,capitalPerStock,ltp):
    Margin = getMargin(ticker)
    tradeQuantity = int((capitalPerStock*Margin)/ltp)
    return tradeQuantity

# q = tradeQuantity("HDFC",250000,1600)
# print(q)

def EmaCrossOver(ohlc):
    print("Signal functon run at -"+ str(ohlc.index[-1]))
    global upward_sma_dir
    global downward_sma_dir
    global signal
    ohlc = RSI(ohlc,14)
    ohlc["5EMA"]=round(ohlc["close"].ewm(span=5,min_periods=5).mean(),2)
    ohlc["10EMA"]=round(ohlc["close"].ewm(span=10,min_periods=10).mean(),2)
    ohlc = ohlc.loc[:,["open","high","low","close","RSI","5EMA","10EMA","last_price","instrument_token"]]
    if ohlc["5EMA"].iloc[-2] > ohlc['10EMA'].iloc[-2] and ohlc["5EMA"].iloc[-3] < ohlc['10EMA'].iloc[-3] and (ohlc["RSI"].iloc[-2]>55 and ohlc["last_price"].iloc[-1] > ohlc["average_price"].iloc[-1]):
        upward_sma_dir = 'True'
        downward_sma_dir = 'False'
    if ohlc["5EMA"].iloc[-2] < ohlc['10EMA'].iloc[-2] and ohlc["5EMA"].iloc[-3] > ohlc['10EMA'].iloc[-3] and (ohlc["RSI"].iloc[-2]<47 and ohlc["last_price"].iloc[-1] < ohlc["average_price"].iloc[-1]):
        upward_sma_dir= 'False'
        downward_sma_dir = 'True'  
    if upward_sma_dir == 'True':
        qry = "insert into Signal(Instrument,Signal,Time,BuyAt,Target) values(?,?,?,?,?);"
        cursor.execute(qry ,(int(ohlc["instrument_token"].iloc[-1]),"BUY",datetime.strptime(str(ohlc.index[-1]),'%Y-%m-%d %H:%M:%S'),ohlc["close"].iloc[-1],ohlc["close"].iloc[-1]+2))
        con.sqlit.commit()
        signal = 'Buy'
    if downward_sma_dir == 'True':
        qry = "insert into Signal(Instrument,Signal,Time,BuyAt,Target) values(?,?,?,?,?);"
        cursor.execute(qry ,(int(ohlc["instrument_token"].iloc[-1]),"SELL",datetime.strptime(str(ohlc.index[-1]), '%Y-%m-%d %H:%M:%S'),ohlc["close"].iloc[-1],ohlc["close"].iloc[-1]-2))
        con.sqlit.commit() 
        signal = 'Sell'
    return  signal  
               



    

