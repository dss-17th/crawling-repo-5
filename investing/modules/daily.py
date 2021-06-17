import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import requests
import time
import re


def crawlingquery(symbol):
    url = f"https://investing.com/search/?q={symbol}"
    headers = {"User-Agent" : "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # 맞는 데이터 찾기
    dom = BeautifulSoup(response.content, "html.parser")
    datas = dom.find_all(class_ = "js-inner-all-results-quote-item row")
    investing_query = np.nan

    for i in range(len(datas)):
        flag = datas[i].find(class_= "flag first")
        try:
            if re.findall('middle (USA)',str(flag))[0] != 'USA':
                continue
        except:
            continue

        investingsymbol = datas[i].find(class_= "second").text
        if investingsymbol.upper() != symbol.upper() :
            continue

        text = datas[i].find(class_= "fourth").text
        if text[:5] != 'Stock':
            continue


        investing_query = re.findazll('equities\/([\S]+)', datas[i].get("href"))[0]
        return investing_query

def crawling_investing(symbol, query):
    try : 
        url = f"https://kr.investing.com/equities/{query}"
        headers = {"User-Agent" : "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        dom = BeautifulSoup(response.content, "html.parser")
        elements = dom.find_all(class_ ='flex justify-between border-b py-2 desktop:py-0.5')
        time.sleep(3)
        for element in elements:
            try:
                str = re.findall('발행주식수([0-9\,]+)' , element.text)[0]
                shared = int(str.replace(',', ''))
            except:
                pass
            
            try : 
                sales = re.findall('매출([0-9\.A-Z]+)',element.text)[0]
                float(sales[:-1])* int(sales[-1].replace('B', str(10000*10000*10)).replace('M' , str(10000*100)))
            except:
                pass
            
            try:
                str = re.findall('다음 수익일자([0-9년월일\s]+)' , element.text)[0]
                year = int(re.findall('(2[12])년',str)[0])
                month = int(re.findall('([0-9]{1,2})월',str)[0])
                date = int(re.findall('([0-9]{1,2})일',str)[0])
                update_date = year*10000 + month*100 + date + 1
            except:
                continue
                
        return [symbol, sales, shared, update_date]
                
    except :
        return [symbol, np.nan, np.nan, np.nan]

def crawling_investing2(symbol, query):
    first_date = first_sales= first_profit= first_operating= first_realprofit= second_date= second_sales= second_profit= second_operating= second_realprofit= thirth_date= thirth_sales= thirth_profit= thirth_operating=thirth_realprofit= fourth_date= fourth_sales= fourth_profit= fourth_operating= fourth_realprofit = np.nan
    try : 
        url = f"https://kr.investing.com/equities/{query}-financial-summary"
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        response = requests.get(url, headers=headers)
        dom = BeautifulSoup(response.content, "html.parser")
        dates = dom.select("#rsdiv > div > table > thead > tr > th")
        numbers = dom.select("#rsdiv > div > table > tbody > tr > td")
        time.sleep(2)
        
        for date, i in zip(dates, range(len(dates))) :
            if date.text == '기말:':
                str = re.findall('[0-9년월일\s]+' , dates[i+1].text)[0]
                year = int(re.findall('(2[0-9])년',str)[0])
                month = int(re.findall('([0-9]{1,2})월',str)[0])
                day = int(re.findall('([0-9]{1,2})일',str)[0])
                first_date = year*10000 + month*100 + day
                str = re.findall('[0-9년월일\s]+' , dates[i+2].text)[0]
                year = int(re.findall('(2[0-9])년',str)[0])
                month = int(re.findall('([0-9]{1,2})월',str)[0])
                day = int(re.findall('([0-9]{1,2})일',str)[0])
                second_date = year*10000 + month*100 + day
                str = re.findall('[0-9년월일\s]+' , dates[i+3].text)[0]
                year = int(re.findall('(2[0-9])년',str)[0])
                month = int(re.findall('([0-9]{1,2})월',str)[0])
                day = int(re.findall('([0-9]{1,2})일',str)[0])
                thirth_date = year*10000 + month*100 + day
                str = re.findall('[0-9년월일\s]+' , dates[i+4].text)[0]
                year = int(re.findall('(2[0-9])년',str)[0])
                month = int(re.findall('([0-9]{1,2})월',str)[0])
                day = int(re.findall('([0-9]{1,2})일',str)[0])
                fourth_date = year*10000 + month*100 + day
                break
                     
                    
        for number, i in zip(numbers, range(len(numbers))) :
            if number.text == '총매출':
                try : 
                    first_sales = float(numbers[i+1].text)
                    second_sales = float(numbers[i+2].text)
                    thirth_sales = float(numbers[i+3].text)
                    fourth_sales = float(numbers[i+4].text)
                except : 
                    first_sales =  second_sales = thirth_sales = fourth_sales = np.nan
            elif number.text == '총 이익':
                try : 
                    first_profit = float(numbers[i+1].text)
                    second_profit = float(numbers[i+2].text)
                    thirth_profit = float(numbers[i+3].text)
                    fourth_profit = float(numbers[i+4].text)
                except :
                    first_profit = second_profit = thirth_profit =  fourth_profit = np.nan
                
            elif number.text == '영업 이익':
                try :
                    first_operating = float(numbers[i+1].text)
                    second_operating = float(numbers[i+2].text)
                    thirth_operating = float(numbers[i+3].text)
                    fourth_operating = float(numbers[i+4].text)
                except :
                    first_operating = second_operating = thirth_operating = fourth_operating = np.nan


            elif number.text == '순이익':
                try : 
                    first_realprofit = float(numbers[i+1].text)
                    second_realprofit = float(numbers[i+2].text)
                    thirth_realprofit = float(numbers[i+3].text)
                    fourth_realprofit = float(numbers[i+4].text)
                except:
                    first_realprofit = second_realprofit = thirth_realprofit = fourth_realprofit = np.nan

        dfs = [symbol, first_date, first_sales, first_profit, first_operating, first_realprofit, \
                   second_date, second_sales, second_profit, second_operating, second_realprofit, \
                   thirth_date, thirth_sales, thirth_profit, thirth_operating, thirth_realprofit, \
                   fourth_date, fourth_sales, fourth_profit, fourth_operating, fourth_realprofit,]

                
    except :
        dfs = [symbol, np.nan, np.nan, np.nan, np.nan, np.nan, \
                   np.nan, np.nan, np.nan, np.nan, np.nan, \
                   np.nan, np.nan, np.nan, np.nan, np.nan, \
                   np.nan, np.nan, np.nan, np.nan, np.nan,]

    return dfs



querys = pd.read_csv('../datas/investing_query.csv')

investing = pd.read_csv
today = datetime.now().year % 100 * 10000 + datetime.now().month * 100  +  datetime.now().day
df = []
crawling_investings = []
crawling_investings2 = []
a = 0
for row in querys.values:
    symbol = row[0]
    query = row[1]
    update_date = row[2]
    url = f"https://kr.investing.com/equities/{query}-news"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code >= 300 :
        a = 1
        query = crawlingquery(symbol)
        querys['investing_query'][querys['Symbol'] == symbol] = query 
        url = f"https://kr.investing.com/equities/{query}-news"
        response = requests.get(url, headers=headers)
        if response.status_code >= 300 :
            print(f'{symbol}의 서버가 응답하지 않습니다. 에러 코드 {response.status_code}')
    
    dom = BeautifulSoup(response.content, "html.parser")
    datas = dom.find_all(class_ = "textDiv")

    for i in range(len(datas)):
        item = datas[i]
        try : 
            text = item.select_one('.date').text
            date = re.findall('[0-9]{0,2} 시간 전',text)
        except:
            continue
        title = item.select_one(".title").get("title")
        link = 'https://kr.investing.com' + item.select_one(".title").get("href")
        if date != []:
            df.append({'symbol':symbol, 'title':title, "link":link, 'date':date})
    time.sleep(0.5)

    
    if today >= update_date :
        crawling_investings.append(crawling_investing(symbol, query))
        crawling_investings2.append(crawling_investing2(symbol, query))

try : 
    crawling_investings[0]
    datas = crawling_investings
    
except:
    pass
else : 
    crawling_investings = pd.read_csv('../datas/crawling_investing.csv')
    
    for data in datas :
        crawling_investings[crawling_investings['symbol'] == data[0]] = data
        querys['update_date'][querys['symbol'] == data[0]] = data[3]
        
    crawling_investings.to_csv('../datas/crawling_investing.csv', index=False)
    print('update crawling_investing')
    a = 1

try : 
    crawling_investings2[0]
    datas = crawling_investings2
    
except:
    pass
else : 
    crawling_investings2 = pd.read_csv('../datas/crawling_investing2.csv')
    
    for data in datas :
        crawling_investings2[crawling_investings2['symbol'] == data[0]] =  data
        
    crawling_investings2.to_csv('../datas/crawling_investing.csv', index=False)
    print('update crawling_investing2')
    a = 1
        
df= pd.DataFrame(df) 
df.to_csv('../datas/investing_news.csv', index=False)

if a == 1 : 
    querys.to_csv('../datas/investing_query.csv', index=False)