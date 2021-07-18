from flask import *
from app.modules import MysqlModule
from app import app

@app.route('/SP500')
def sp():
    db_class= MysqlModule.Database()

## 1. s&p500 종가 시계열 그래프
    sql1 = "SELECT * \
    FROM daily \
    WHERE Symbol = 'US500';"
    data1 = db_class.executeAll(sql1)

    x_label = [data['Date'] for data in data1]
    y_closed = [data['Close'] for data in data1]

## 2. 섹터별 일일 거래량 비율aaaaaa
    sql2 = "SELECT Sector, AVG(Volume) as sector_volume \
    FROM US_Stock.company, US_Stock.daily \
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol \
    and DATE(Date)= '2021-06-10' and US_Stock.company.Sector != 'None' \
    GROUP BY Sector \
    ORDER BY AVG(Volume) DESC;";
    
    data2 = db_class.executeAll(sql2)

    sect = [data['Sector'] for data in data2]
    volumes = [data['sector_volume'] for data in data2]

## 3. 섹터별 시가총액 차트 testesetasldkfjaslkfjalskdjflakjsdlfj
    sql3 = "SELECT Sector, SUM(market capitalization) as market_capital \
    FROM US_Stock.company, US_Stock.daily \
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol \
    and DATE(Date)= '2021-06-10' and US_Stock.company.Sector != 'None'\
    GROUP BY Sector \
    ORDER BY sum(market capitalization) DESC;"

    data3 = db_class.executeAll(sql3)
    
    sector = []
    capital = []

    for data in data3:
        sector.append(data['Sector'])
        capital.append(data['market_capital'])

    
    return render_template('index_sp.html', x_data=x_label, y_data=y_closed, x_data2=sect, y_data2=volumes, x_data3=sector,y_data3=capital)