import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import warnings
import pandas as pd
import FinanceDataReader as fdr
import numpy as np
from datetime import datetime, timedelta
import time
warnings.filterwarnings(action='ignore')

symbol_list = ["MMM","ABT","ABBV","ABMD","ACN","ATVI","ADBE","AMD","AAP",\
               "AES","AFL","A","APD","AKAM","ALK","ALB","ARE","ALXN","ALGN",\
               "ALLE","LNT","ALL","GOOGL","GOOG","MO","AMZN","AMCR","AEE","AAL",\
               "AEP","AXP","AIG","AMT","AWK","AMP","ABC","AME","AMGN","APH","ADI",\
               "ANSS","ANTM","AON","AOS","APA","AAPL","AMAT","APTV","ADM","ANET","AJG",\
               "AIZ","T","ATO","ADSK","ADP","AZO","AVB","AVY","BKR","BLL","BAC","BK","BAX",\
               "BDX","BRKB","BBY","BIO","BIIB","BLK","BA","BKNG","BWA","BXP","BSX","BMY","AVGO",\
               "BR","BFB","CHRW","COG","CDNS","CZR","CPB","COF","CAH","KMX","CCL","CARR","CTLT","CAT"\
               ,"CBOE","CBRE","CDW","CE","CNC","CNP","CERN","CF","CRL","SCHW","CHTR","CVX","CMG","CB","CHD",\
               "CI","CINF","CTAS","CSCO","C","CFG","CTXS","CLX","CME","CMS","KO","CTSH","CL","CMCSA","CMA","CAG",\
               "COP","ED","STZ","COO","CPRT","GLW","CTVA","COST","CCI","CSX","CMI","CVS","DHI","DHR","DRI","DVA","DE",\
               "DAL","XRAY","DVN","DXCM","FANG","DLR","DFS","DISCA","DISCK","DISH","DG","DLTR","D","DPZ","DOV","DOW","DTE",\
               "DUK","DRE","DD","DXC","EMN","ETN","EBAY","ECL","EIX","EW","EA","EMR","ENPH","ETR","EOG","EFX","EQIX","EQR","ESS",\
               "EL","ETSY","EVRG","ES","RE","EXC","EXPE","EXPD","EXR","XOM","FFIV","FB","FAST","FRT","FDX","FIS","FITB","FE","FRC",\
               "FISV","FLT","FMC","F","FTNT","FTV","FBHS","FOXA","FOX","BEN","FCX","GPS","GRMN","IT","GNRC","GD","GE","GIS","GM","GPC",\
               "GILD","GL","GPN","GS","GWW","HAL","HBI","HIG","HAS","HCA","PEAK","HSIC","HSY","HES","HPE","HLT","HOLX","HD","HON",\
               "HRL","HST","HWM","HPQ","HUM","HBAN","HII","IEX","IDXX","INFO","ITW","ILMN","INCY","IR","INTC","ICE","IBM","IP","IPG","IFF",\
               "INTU","ISRG","IVZ","IPGP","IQV","IRM","JKHY","J","JBHT","SJM","JNJ","JCI","JPM","JNPR","KSU","K","KEY","KEYS","KMB","KIM","KMI",\
               "KLAC","KHC","KR","LB","LHX","LH","LRCX","LW","LVS","LEG","LDOS","LEN","LLY","LNC","LIN","LYV","LKQ","LMT","L","LOW","LUMN","LYB",\
               "MTB","MRO","MPC","MKTX","MAR","MMC","MLM","MAS","MA","MKC","MXIM","MCD","MCK","MDT","MRK","MET","MTD","MGM","MCHP","MU","MSFT","MAA",\
               "MHK","TAP","MDLZ","MPWR","MNST","MCO","MS","MOS","MSI","MSCI","NDAQ","NTAP","NFLX","NWL","NEM","NWSA","NWS","NEE","NLSN","NKE","NI","NSC",\
               "NTRS","NOC","NLOK","NCLH","NOV","NRG","NUE","NVDA","NVR","NXPI","ORLY","OXY","ODFL","OMC","OKE","ORCL","OTIS","PCAR","PKG","PH","PAYX","PAYC",\
               "PYPL","PENN","PNR","PBCT","PEP","PKI","PRGO","PFE","PM","PSX","PNW","PXD","PNC","POOL","PPG","PPL","PFG","PG","PGR","PLD","PRU","PTC","PEG","PSA",\
               "PHM","PVH","QRVO","PWR","QCOM","DGX","RL","RJF","RTX","O","REG","REGN","RF","RSG","RMD","RHI","ROK","ROL","ROP","ROST","RCL","SPGI","CRM","SBAC",\
               "SLB","STX","SEE","SRE","NOW","SHW","SPG","SWKS","SNA","SO","LUV","SWK","SBUX","STT","STE","SYK","SIVB","SYF","SNPS","SYY","TMUS","TROW","TTWO","TPR",\
               "TGT","TEL","TDY","TFX","TER","TSLA","TXN","TXT","TMO","TJX","TSCO","TT","TDG","TRV","TRMB","TFC","TWTR","TYL","TSN","UDR","ULTA","USB","UAA","UA","UNP",\
               "UAL","UNH","UPS","URI","UHS","UNM","VLO","VTR","VRSN","VRSK","VZ","VRTX","VFC","VIAC","VTRS","V","VNO","VMC","WRB","WAB","WMT","WBA","DIS","WM","WAT","WEC",\
               "WFC","WELL","WST","WDC","WU","WRK","WY","WHR","WMB","WLTW","WYNN","XEL","XLNX","XYL","YUM","ZBRA","ZBH","ZION","ZTS","US500"]

%%time
start = time.time() # 시작시간 저장
yesterday = datetime.today() - timedelta(1)

apple = fdr.DataReader("AAPL",start="2021-07-30", end="2021-07-30") # fdr 기존 양식에 symbol_list를 추가하기 위해 base_table 생성
apple

dfs = apple
dfs['Symbol'] = "AAPL"

symbol_list

for i in symbol_list: # apple data frame에 symbol_list 추가작업 진행
    data = fdr.DataReader(i, start="2021-07-29", end="2021-07-29")
    df = pd.DataFrame(data)
    df['Symbol'] = i
    dfs = pd.concat([df,dfs])

dfs = dfs[['Symbol', 'Close', "Open", "High", "Low", "Volume", "Change"]]
dfs = dfs.reset_index() # reset_index()를 사용해 date column에 위치하게 정렬
dfs = dfs.drop_duplicates(['Symbol', 'Close', "Open", "High", "Low", "Volume", "Change"]) # 상단에 생성한 중복된 apple 정보 삭제
print(dfs)
print("time :", time.time() - start) # 현재시각 - 시작시간 = 실행시간

us_stock_basedata = pd.read_csv('./amount_to_be registered.csv') # frd에 없는 data csv로 import
us_stock_basedata

daily = pd.merge(dfs,us_stock_basedata, how='left', on='Symbol') # frd와 csv merge 작업 기준은 symbol로 잡아 왼쪽으로 정렬
daily

daily["market_capitalization"] = daily["Close"]*daily["amount_to_be_registered"]
daily

a=daily.rename(columns={"Change":"Changee"})

b=a.rename(columns={'index':'Date'})

b

daily.to_csv('daily_210730_2.csv')

#1. mysqldb 접속객체 세팅(연결하기)
connect_datas = {
    'host': '34.134.233.184',
    'user': 'root',
    'passwd': 'dss',
    'db': 'US_Stock',
    'charset': 'utf8'
}
db = MySQLdb.connect(**connect_datas)
db

#2. 주가데이터 csv파일 불러오기
stock = pd.DataFrame(b)
#stock_df = stock.drop(columns='Unnamed: 0')
#stock.rename(columns={'Change':'Changee'})
#stock_df.rename(columns={'index':'Date'})
stock

# # MYsqldb로 테이블 생성하기
# QUERY = """
#     CREATE TABLE daily (
#     Date DATE,
#     Symbol Varchar(5) NOT NULL,
#     Close INT(30) NOT NULL,
#     Open INT(30)NOT NULL,
#     High INT(30) NOT NULL,
#     Low INT(30)NOT NULL,
#     Volume INT(30)NOT NULL,
#     Changee Varchar(30),
#     amount_to_be_registered INT(100),
#     market_capitalization DOUBLE,
#     FOREIGN KEY (Symbol) REFERENCES company(Symbol)
#     )
# """
# # cursor객체 생성후 쿼리 실행
# curs = db.cursor()
# curs.execute(QUERY)

#3. sqlalchemy 클라이언트 설정
client = create_engine('mysql://root:dss@34.134.233.184/US_Stock?charset=utf8',encoding="utf-8")
conn = client.connect()

#4. csv파일 db에 담기(Daily file)
stock.to_sql(name='daily',con=client, if_exists='append',index=False)
conn.close()



