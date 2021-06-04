import numpy as np
import requests
from bs4 import BeautifulSoup
import re
symbols = pd.read_csv('symbol.csv')
frames = []
a = 1

for data in symbols.values:
    symbol = data[0]
    name = data[1]
    url = f"https://investing.com/search/?q={symbol}"
    headers = {"User-Agent" : ""}
    response = requests.get(url, headers=headers)
    time.sleep(1)
    

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
        
        #investingname = datas[i].find(class_= "third").text
        #if investingname != name :
        #    continue
        
        text = datas[i].find(class_= "fourth").text
        if text[:5] != 'Stock':
            continue
        
        
        investing_query = re.findall('equities\/([0-9a-zA-Z\-]+)', datas[i].get("href"))[0]
        frames.append([symbol, investing_query])
        #break
        
    if a != len(frames) :
        print([a, len(frames)])
        break
    print(a)
    a += 1
    
dfs = pd.DataFrame(dfs)
dfs.replace(columns = {0:'Symbol', 1:'Query'})
dfs.to_csv('investing_query')
