import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import urllib3 
import io

rem_thousand_sep_and_cast_to_float = lambda x: pd.np.float(x.replace(",", "")) 
URL = "https://www.nseindia.com/api/market-data-pre-open?key=NIFTY&csv=true"
headers = {"accept-encoding": "gzip, deflate, br",
           "accept-language": "en-US,en;q=0.9,hi;q=0.8,ms;q=0.7",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
          }
cookie_dict = {"bm_sv":"9ED953DE41A802B656B8D5817D30E0E5~nDmAt+hEjI8C0MgRx9ODK7YlVGfPWDCvCjjYL8wMoXHGOYq1MX4+fbI5Dkc1PVkLflFvg9mE69gs/CHkg1SXX4RIvjbcxh1tLmNfd+7lR85zghx9m+yLoWs+kyf8/K4k4C23Dv0UP4AjucU17gaY0dQSaHQJ0dBXipvrX1CoVis="}          
session = rq.session()
for cookie in cookie_dict:
    session.cookies.set(cookie,cookie_dict[cookie])
x = session.get(URL,headers = headers)
open('DATA.csv', 'wb').write(x.content)
# csv = pd.read_csv("DATA.csv" , thousands=","
#                              ,converters={"IEP  PRICE \n": rem_thousand_sep_and_cast_to_float})

csv = pd.io.parsers.read_csv("DATA.csv", sep=",", thousands=",",
                            converters={"IEP  PRICE \n": rem_thousand_sep_and_cast_to_float})  

new_csv = csv.rename(columns = {'SYMBOL \n' : "SYMBOL", 'PREV. CLOSE \n' :"PREV. CLOSE", 'IEP  PRICE \n' :"IEPPRICE" , 'CHNG \n' : "CHNG", '%CHNG \n':"%CHNG",
                                'FINAL PRICE \n' : "FINAL PRICE", 'FINAL QUANTITY \n' : "FINAL QUANTITY", 'VALUE ' : "VALUE", 'FFM CAP ' : "FFM CAP",
                                'NM 52W H \n' : "NM 52W H", 'NM 52W L \n' : "NM 52W L"}) 

# ['SYMBOL \n', 'PREV. CLOSE \n', 'IEP  PRICE \n', 'CHNG \n', '%CHNG \n',
#        'FINAL PRICE \n', 'FINAL QUANTITY \n', 'VALUE ', 'FFM CAP ',
#        'NM 52W H \n', 'NM 52W L \n']


new_csv["%CHNG"].replace({"-": "0"}, inplace=True)
new_csv[["%CHNG"]] = new_csv[["%CHNG"]].apply(pd.to_numeric)
tot =  new_csv["%CHNG"].sum()
if(tot < 0):
    new_csv = new_csv[new_csv["%CHNG"]<-1]
    new_csv = new_csv[new_csv["%CHNG"]>=-1.4]
    new_csv = new_csv[new_csv["FINAL QUANTITY"]>20000]
    new_csv=new_csv.drop(columns=["PREV. CLOSE","IEPPRICE","CHNG","FINAL PRICE","FINAL QUANTITY","VALUE","FFM CAP","NM 52W H","NM 52W L"])
elif (tot > 0):
    new_csv = new_csv[new_csv["%CHNG"]>1]
    new_csv = new_csv[new_csv["%CHNG"]<=1.4]
    new_csv = new_csv[new_csv["FINAL QUANTITY"]>20000]
    new_csv=new_csv.drop(columns=["PREV. CLOSE","IEPPRICE","CHNG","FINAL PRICE","FINAL QUANTITY","VALUE","FFM CAP","NM 52W H","NM 52W L"])
print(new_csv)
new_csv.to_csv('SelectedStocks.csv')


