import MysqlModule
import pickle

db_class= MysqlModule.Database()

## 1. s&p500 종가 시계열 그래프
sql1 = f"SELECT date_format(daily.Date, '%%Y-%%m-%%d') as Date, Close \
FROM daily \
WHERE Symbol = 'US500';"
data1 = db_class.executeAll(sql1)

x_label = [data['Date'] for data in data1]
y_closed = [data['Close'] for data in data1]

## 2. 섹터별 일일 거래량 비율
sql2 = "SELECT Sector, AVG(Volume) as sector_volume \
FROM US_Stock.company, US_Stock.daily \
WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol \
and DATE(Date)= '2021-06-10' and US_Stock.company.Sector != 'None' \
GROUP BY Sector \
ORDER BY AVG(Volume) DESC;"

data2 = db_class.executeAll(sql2)

sect = [data['Sector'] for data in data2]
volumes = [float(data['sector_volume']) for data in data2]

#<<<<<<< HEAD
## 3. 섹터별 시가총액 차트 testesetasldkfjaslkfjalskdjflakjsdlfj
#=======
## 3. 섹터별 시가총액 차트 
#>>>>>>> da4a38f8623d59a700b84688e1fa4ad68ade24e0
sql3 = "SELECT Sector, SUM(market_capitalization) as market_capital \
FROM US_Stock.company, US_Stock.daily \
WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol \
and DATE(Date)= '2021-06-10' and US_Stock.company.Sector != 'None'\
GROUP BY Sector \
ORDER BY sum(market_capitalization) DESC;"

data3 = db_class.executeAll(sql3)

sector = []
capital = []

for data in data3:
    sector.append(data['Sector'])
    capital.append(data['market_capital'])

## 4,5,6,7 테이블
sql4 = "SELECT daily.Symbol, company.Name, SUM((Close-Open)/Open) as Changes \
FROM US_Stock.daily \
INNER JOIN US_Stock.company \
ON daily.Symbol = company.Symbol \
WHERE DATE(Date) >= DATE_SUB('2021-06-28', INTERVAL 1 DAY) \
GROUP BY daily.Symbol \
ORDER BY Changes DESC;"

table1 = db_class.executeAll(sql4)

sql5 = "SELECT daily.Symbol, company.Name, SUM((Close-Open)/Open) as Changes \
FROM US_Stock.daily \
INNER JOIN US_Stock.company \
ON daily.Symbol = company.Symbol \
WHERE DATE(Date) >= DATE_SUB('2021-06-28', INTERVAL 1 MONTH) \
GROUP BY daily.Symbol \
ORDER BY Changes DESC;"

table2 = db_class.executeAll(sql5)

sql6 = "SELECT daily.Symbol, company.Name, SUM((Close-Open)/Open) as Changes \
FROM US_Stock.daily \
INNER JOIN US_Stock.company \
ON daily.Symbol = company.Symbol \
WHERE DATE(Date) >= DATE_SUB('2021-06-28', INTERVAL 3 MONTH) \
GROUP BY daily.Symbol \
ORDER BY Changes DESC;"

table3 = db_class.executeAll(sql6)

sql7 = "SELECT daily.Symbol, company.Name, SUM((Close-Open)/Open) as Changes \
FROM US_Stock.daily \
INNER JOIN US_Stock.company \
ON daily.Symbol = company.Symbol \
WHERE DATE(Date) >= DATE_SUB('2021-06-28', INTERVAL 1 YEAR) \
GROUP BY daily.Symbol \
ORDER BY Changes DESC;"

table4 = db_class.executeAll(sql7)


datas = (capital, sector, volumes, sect, y_closed, x_label, table4, table3, table2, table1)
print(type(datas))
with open('datas.pickle', 'wb') as f:
    pickle.dump(datas, f)
