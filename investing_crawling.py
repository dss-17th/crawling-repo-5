import time
import re

dfs = []
a = 1
for data in datas.values:
    symbol = data[0]
    query = data[1]
    try : 
        url = f"https://kr.investing.com/equities/{query}"
        headers = {"User-Agent" : " "}
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
                
        dfs.append([symbol, sales, shared, update_date])
        print(a)
        a += 1
                
    except :
        dfs.append([symbol, np.nan, np.nan, np.nan])
        print(a)
        a += 1

dfs = pd.DataFrame(dfs)
dfs = dfs.replace(columns={0:'symbol', 1:'sales', 2:'shared', 3:'update_date'})
dfs.to_csv('crawling_investing')