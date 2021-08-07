import re
import requests
import numpy as np
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import warnings     
warnings.filterwarnings(action='ignore')    
import user
path = user.path

def crawlingquery(symbol):
    url = f"https://investing.com/search/?q={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # 맞는 데이터 찾기
    dom = BeautifulSoup(response.content, "html.parser")
    datas = dom.find_all(class_="js-inner-all-results-quote-item row")
    investing_query = np.nan

    for i in range(len(datas)):
        flag = datas[i].find(class_="flag first")
        try:
            if re.findall('middle (USA)', str(flag))[0] != 'USA':
                continue
        except:
            continue

        investingsymbol = datas[i].find(class_="second").text
        if investingsymbol.upper() != symbol.upper():
            continue

        text = datas[i].find(class_="fourth").text
        if text[:5] != 'Stock':
            continue

        investing_query = re.findall(
            'equities\/([\S]+)', datas[i].get("href"))[0]
        return investing_query


def crawling_investing(query):
    try:
        url = f"https://kr.investing.com/equities/{query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        dom = BeautifulSoup(response.content, "html.parser")
        elements = dom.find_all(
            class_='flex justify-between border-b py-2 desktop:py-0.5')
        # time.sleep(0.5)
        for element in elements:
            try:
                shared = re.findall('발행주식수([0-9\,]+)', element.text)[0]
                shared = int(shared.replace(',', ''))
            except:
                pass

            try:
                sales = re.findall('매출([0-9\.A-Z]+)', element.text)[0]
                sales = float(sales[:-1]) * int(sales[-1].replace('B', str(10000*10000*10)).replace('M', str(10000*100)))
            except:
                pass

            try:
                data = re.findall('다음 수익일자([0-9년월일\s]+)', element.text)[0]
                year = int(re.findall('(2[12])년', data)[0])
                month = int(re.findall('([0-9]{1,2})월', data)[0])
                date = int(re.findall('([0-9]{1,2})일', data)[0])
                update_date = year*10000 + month*100 + date
                update_date = datetime.datetime.strptime(str(update_date), '%y%m%d') + datetime.timedelta(days=1)
            except:
                continue
            
            
            
        return [sales, shared, update_date]

    except:
        return [np.nan, np.nan, np.nan]

def crawling_investing2(query):
    querys = pd.read_csv(path + 'investing_query.csv')
    symbol = querys['symbol'][querys['query'] == query].values[0]
    first_date = first_sales = first_profit = first_operating = first_realprofit = second_date = second_sales = second_profit = second_operating = second_realprofit = thirth_date = thirth_sales = thirth_profit = thirth_operating = thirth_realprofit = fourth_date = fourth_sales = fourth_profit = fourth_operating = fourth_realprofit = np.nan
    try:
        url = f"https://kr.investing.com/equities/{query}-financial-summary"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response = requests.get(url, headers=headers)
        dom = BeautifulSoup(response.content, "html.parser")
        dates = dom.select("#rsdiv > div > table > thead > tr > th")
        numbers = dom.select("#rsdiv > div > table > tbody > tr > td")
        # time.sleep(0.5)

        for date, i in zip(dates, range(len(dates))):
            if date.text == '기말:':
                data = re.findall('[0-9년월일\s]+', dates[i+1].text)[0]
                year = int(re.findall('(2[0-9])년', data)[0])
                month = int(re.findall('([0-9]{1,2})월', data)[0])
                day = int(re.findall('([0-9]{1,2})일', data)[0])
                first_date = year*10000 + month*100 + day
                data = re.findall('[0-9년월일\s]+', dates[i+2].text)[0]
                year = int(re.findall('(2[0-9])년', data)[0])
                month = int(re.findall('([0-9]{1,2})월', data)[0])
                day = int(re.findall('([0-9]{1,2})일', data)[0])
                second_date = year*10000 + month*100 + day
                data = re.findall('[0-9년월일\s]+', dates[i+3].text)[0]
                year = int(re.findall('(2[0-9])년', data)[0])
                month = int(re.findall('([0-9]{1,2})월', data)[0])
                day = int(re.findall('([0-9]{1,2})일', data)[0])
                thirth_date = year*10000 + month*100 + day
                data = re.findall('[0-9년월일\s]+', dates[i+4].text)[0]
                year = int(re.findall('(2[0-9])년', data)[0])
                month = int(re.findall('([0-9]{1,2})월', data)[0])
                day = int(re.findall('([0-9]{1,2})일', data)[0])
                fourth_date = year*10000 + month*100 + day
                break

        for number, i in zip(numbers, range(len(numbers))):
            if number.text == '총매출':
                try:
                    first_sales = float(numbers[i+1].text)
                    second_sales = float(numbers[i+2].text)
                    thirth_sales = float(numbers[i+3].text)
                    fourth_sales = float(numbers[i+4].text)
                except:
                    first_sales = second_sales = thirth_sales = fourth_sales = np.nan
            elif number.text == '총 이익':
                try:
                    first_profit = float(numbers[i+1].text)
                    second_profit = float(numbers[i+2].text)
                    thirth_profit = float(numbers[i+3].text)
                    fourth_profit = float(numbers[i+4].text)
                except:
                    first_profit = second_profit = thirth_profit = fourth_profit = np.nan

            elif number.text == '영업 이익':
                try:
                    first_operating = float(numbers[i+1].text)
                    second_operating = float(numbers[i+2].text)
                    thirth_operating = float(numbers[i+3].text)
                    fourth_operating = float(numbers[i+4].text)
                except:
                    first_operating = second_operating = thirth_operating = fourth_operating = np.nan

            elif number.text == '순이익':
                try:
                    first_realprofit = float(numbers[i+1].text)
                    second_realprofit = float(numbers[i+2].text)
                    thirth_realprofit = float(numbers[i+3].text)
                    fourth_realprofit = float(numbers[i+4].text)
                except:
                    first_realprofit = second_realprofit = thirth_realprofit = fourth_realprofit = np.nan
    
#        return first_date, first_sales, first_profit, first_operating, first_realprofit
        dfs1 = [symbol, first_date, first_sales,
                first_profit, first_operating, first_realprofit]
        dfs2 = [symbol, second_date, second_sales,
                second_profit, second_operating, second_realprofit]
        dfs3 = [symbol, thirth_date, thirth_sales,
                thirth_profit, thirth_operating, thirth_realprofit]
        dfs4 = [symbol, fourth_date, fourth_sales,
                fourth_profit, fourth_operating, fourth_realprofit]

    except:
#        return np.nan, np.nan, np.nan, np.nan, np.nan
        dfs1 = [symbol, np.nan, np.nan, np.nan, np.nan, np.nan]
        dfs2 = [symbol, np.nan, np.nan, np.nan, np.nan, np.nan]
        dfs3 = [symbol, np.nan, np.nan, np.nan, np.nan, np.nan]
        dfs4 = [symbol, np.nan, np.nan, np.nan, np.nan, np.nan]

    return dfs1, dfs2, dfs3, dfs4


querys = pd.read_csv(path + 'investing_query.csv')

investing = pd.read_csv
today = datetime.datetime.now().year * 10000 + datetime.datetime.now().month * 100 + datetime.datetime.now().day
df = []
crawling_investings = []
a = 0
for row in querys.values:
    symbol = row[0]
    query = row[1]
    update_date = querys.values[0][2].split(' ')[0]
    update_date = int(update_date.split('-')[0]) * 10000 + int(update_date.split('-')[1]) * 100 + int(update_date.split('-')[2])
    url = f"https://kr.investing.com/equities/{query}-news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code >= 300:
        a = 1
        query = crawlingquery(symbol)
        querys['query'][querys['symbol'] == symbol] = query
        url = f"https://kr.investing.com/equities/{query}-news"
        response = requests.get(url, headers=headers)
        if response.status_code >= 300:
            print(f'{symbol}의 서버가 응답하지 않습니다. 에러 코드 {response.status_code}')

    dom = BeautifulSoup(response.content, "html.parser")
    datas = dom.find_all(class_="textDiv")

    for i in range(len(datas)):
        item = datas[-i]
        try:
            text = item.select_one('.date').text
            date = re.findall('[0-9]{0,2} 시간 전', text)
        except:
            continue
        title = item.select_one(".title").get("title")
        subtitle = BeautifulSoup(item.select_one('p').text, "html.parser")
        if item.select_one(".title").get("href")[:8] != 'https://':
            link = 'https://kr.investing.com' + item.select_one(".title").get("href")
        else :
            link = item.select_one(".title").get("href")

        df.append({'symbol': symbol, 'title': title, 'subtitle': subtitle,"link": link})
    time.sleep(0.2)

    if today > update_date:
        [sales, shared, update_date]  = crawling_investing(query)
        time.sleep(0.2)
        dfs1, dfs2, dfs3, dfs4 = crawling_investing2(query)
        for k in [sales, shared, update_date]:
            dfs1.append(k)
            dfs2.append(k)
            dfs3.append(k)
            dfs4.append(k)
        crawling_investings.append(dfs1)
        # crawling_investings.append(dfs2)
        # crawling_investings.append(dfs3)
        # crawling_investings.append(dfs4)
        querys['update_date'][querys['symbol'] == symbol] = update_date
        a=1
        

#1. mysqldb 접속객체 세팅(연결하기)
connect_datas = {
    'host': user.host,
    'user': user.user,
    'passwd': user.pw,
    'db': user.db,
    'charset': 'utf8'
}
db = MySQLdb.connect(**connect_datas) 

client = create_engine(f'mysql://{user.user}:{user.pw}@{user.host}/{user.db}?charset=utf8',encoding="utf-8")
conn = client.connect()
##news 데이터 sql에 집어넣기
news = pd.DataFrame(df)
news.columns=['Symbol', 'title', 'subtitle', 'link']
# # # MYsqldb로 테이블 생성하기
# sql = '''CREATE TABLE News ( 
# Symbol varchar(5) NOT NULL, 
# title varchar(200),
# subtitle varchar(200),
# link varchar(200),
# FOREIGN KEY (Symbol) REFERENCES company(Symbol)
# ) 
# ''' 
# # cursor객체 생성후 쿼리 실행
# curs = db.cursor()
# curs.execute(sql)


# nonmaker = querys[['symbol']]
# nonmaker.columns = ['Symbol']
# for column in ['title', 'subtitle', 'link']:
#     nonmaker[column] = np.nan
# news = pd.concat([nonmaker, nonmaker, nonmaker, nonmaker, nonmaker, news])
# news = news.append(pd.DataFrame(['US500'], columns=['Symbol']))
news = news.fillna('-')
news.to_sql(name='News',con=client,if_exists='append',index=False)

## investing 데이터 집어넣기
investing_cr= pd.DataFrame(crawling_investings,columns=["Symbol", 'update_date', 'querter_sales','profit','operating' ,'real_profit','sales' ,'share' ,'next_update_date'])
# investing_cr = investing_cr.append(pd.DataFrame(['US500'], columns=['Symbol']))
# # MYsqldb로 테이블 생성하기
# sql = '''CREATE TABLE Company_low ( 
# Symbol varchar(5) NOT NULL, 
# update_date date, 
# querter_sales double,
# profit double,
# operating double,
# real_profit double,
# sales double,
# share double,
# next_update_date date,
# FOREIGN KEY (Symbol) REFERENCES company(Symbol)
# ) 
# ''' 
# # # cursor객체 생성후 쿼리 실행
# curs = db.cursor()
# curs.execute(sql)

investing_cr.to_sql(name='Company_low',con=client,if_exists='append',index=False)

if a == 1:
    querys.to_csv(path + 'investing_query.csv', index=False)