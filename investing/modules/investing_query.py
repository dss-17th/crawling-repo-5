import numpy as np
import requests
from bs4 import BeautifulSoup
import re


def crawlingquery(symbol):
    url = f"https://investing.com/search/?q={symbol}"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
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