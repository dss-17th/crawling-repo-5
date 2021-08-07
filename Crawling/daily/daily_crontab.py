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
import user
warnings.filterwarnings(action='ignore')

path = user.path
querys = pd.read_csv(path + 'investing_query.csv')
symbol_list = querys['symbol'].values

# %%time
start = time.time() # 시작시간 저장
yesterday = datetime.today() - timedelta(1)
before_yesterday = datetime.today() - timedelta(3)

dfs = fdr.DataReader("US500", start=before_yesterday, end=yesterday) # fdr 기존 양식에 symbol_list를 추가하기 위해 base_table 생성
dfs['Symbol'] = "US500"
for i in symbol_list:
    try:# apple data frame에 symbol_list 추가작업 진행
        data = fdr.DataReader(i, start=before_yesterday, end=yesterday)
        df = pd.DataFrame(data)
        df['Symbol'] = i
        dfs = pd.concat([df,dfs])
    except:
        pass

dfs = dfs[['Symbol', 'Close', "Open", "High", "Low", "Volume", "Change"]]
dfs = dfs.reset_index() # reset_index()를 사용해 date column에 위치하게 정렬
# print(dfs)
# print("time :", time.time() - start) # 현재시각 - 시작시간 = 실행시간

us_stock_basedata = pd.read_csv(path + 'amount_to_be registered.csv') # frd에 없는 data csv로 import
# us_stock_basedata

daily = pd.merge(dfs,us_stock_basedata, how='left', on='Symbol') # frd와 csv merge 작업 기준은 symbol로 잡아 왼쪽으로 정렬
# daily

daily["market_capitalization"] = daily["Close"]*daily["amount_to_be_registered"]
# daily
a=daily.rename(columns={"Change":"Changee"})
b=a.rename(columns={'index':'Date'})
b.to_csv('daily_210730_3.csv')

#1. mysqldb 접속객체 세팅(연결하기)
connect_datas = {
    'host': user.host,
    'user': user.user,
    'passwd': user.pw,
    'db': user.db,
    'charset': 'utf8'
}
db = MySQLdb.connect(**connect_datas)
# db

#2. 주가데이터 csv파일 불러오기
stock = pd.DataFrame(b)
#stock_df = stock.drop(columns='Unnamed: 0')
#stock.rename(columns={'Change':'Changee'})
#stock_df.rename(columns={'index':'Date'})
# stock

# # MYsqldb로 테이블 생성하기
# QUERY = """
#     CREATE TABLE daily (
#     Date DATE,
#     Symbol Varchar(5) NOT NULL,
#     Close INT(30) NOT NULL,
#     Open INT(30)NOT NULL,
#     High INT(30) NOT NULL,
#     Low INT(30)NOT NULL,
#     Volume DOUBLE,
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