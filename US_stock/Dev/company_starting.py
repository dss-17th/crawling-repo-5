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

df_sp500 = fdr.StockListing('sp500') # fdr에서 제공하는 s&p500 기업 정보 출력
df_sp500.loc[505] = ['US500',"S&P500","None","None"]
us_stock_basedata = pd.read_csv('./us_stock_basedata.csv') # frd에 없는 data csv로 import
company = pd.merge(df_sp500,us_stock_basedata, how='inner', on='Symbol') # frd와 csv merge 작업 기준은 symbol로 잡아 왼쪽으로 정렬
#company.to_csv('company_210624.csv')

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

#2. 주가데이터 파일 불러오기
company = pd.DataFrame(company)

# MYsqldb로 테이블 생성하기
QUERY = """
    CREATE TABLE company (
    Symbol Varchar(30) NOT NULL,
    Name Varchar(30) NOT NULL,
    Sector Varchar(30) NOT NULL,
    Industry Varchar(30) NOT NULL,
    Founded Varchar(30) NOT NULL,
    Date first added DATE,
    Headquarters Location Varchar(50) NOT NULL
    )
"""
# cursor객체 생성후 쿼리 실행
curs = db.cursor()
curs.execute(QUERY)

#3. sqlalchemy 클라이언트 설정
client = create_engine('mysql://{}:{}@{}/{}?charset=utf8'.format(user.user, user.pw, user.host, user.db),encoding="utf-8")
conn = client.connect()

#4. csv파일 db에 담기(Daily file)
company.to_sql(name='company',con=client, if_exists='append',index=False)
conn.close()