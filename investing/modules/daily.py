import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import requests
import time
import re
from module import crawlingquery, crawling_investing, crawling_investing2

querys = pd.read_csv('../datas/investing_query.csv')

investing = pd.read_csv
today = datetime.now().year % 100 * 10000 + \
    datetime.now().month * 100 + datetime.now().day
df = []
crawling_investings = []
crawling_investings2 = []
a = 0
for row in querys.values:
    symbol = row[0]
    query = row[1]
    update_date = row[2]
    url = f"https://kr.investing.com/equities/{query}-news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code >= 300:
        a = 1
        query = crawlingquery(symbol)
        querys['investing_query'][querys['Symbol'] == symbol] = query
        url = f"https://kr.investing.com/equities/{query}-news"
        response = requests.get(url, headers=headers)
        if response.status_code >= 300:
            print(f'{symbol}의 서버가 응답하지 않습니다. 에러 코드 {response.status_code}')

    dom = BeautifulSoup(response.content, "html.parser")
    datas = dom.find_all(class_="textDiv")

    for i in range(len(datas)):
        item = datas[i]
        try:
            text = item.select_one('.date').text
            date = re.findall('[0-9]{0,2} 시간 전', text)
        except:
            continue
        title = item.select_one(".title").get("title")
        link = 'https://kr.investing.com' + \
            item.select_one(".title").get("href")
        if date != []:
            df.append({'symbol': symbol, 'title': title,
                       "link": link, 'date': date})
    # time.sleep(0.5)

    if today >= update_date:
        d = crawling_investing(symbol, query)
        crawling_investings.append(d)
        querys['update_date'][querys['Symbol'] == symbol] = d[-1]
        crawling_investings2.append(crawling_investing2(symbol, query))


try:
    crawling_investings[0]

except:
    pass
else:
    crawling_investings.to_csv(
        '../datas/crawling_investing.csv', index=False, header=False, mode='a')
    print('update crawling_investing')
    a = 1


try:
    crawling_investings2[0]
    datas = crawling_investings2
except:
    pass
else:
    crawling_investings2 = pd.DataFrame(datas)
    crawling_investings2.to_csv(
        '../datas/crawling_investing2.csv', index=False, header=False, mode='a')
    print('update crawling_investing2')
    a = 1

df = pd.DataFrame(df)
df.to_csv('../datas/investing_news.csv', index=False, header=False, mode='a')

if a == 1:
    querys.to_csv('../datas/investing_query.csv', index=False)