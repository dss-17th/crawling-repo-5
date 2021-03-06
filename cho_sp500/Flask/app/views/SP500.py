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

## 2. 섹터별 일일 평균거래량
    sql2 = "SELECT Sector, AVG(Volume) as sector_volume \
    FROM US_Stock.company, US_Stock.daily \
    WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol \
    and DATE(Date)= '2021-06-10' and US_Stock.company.Sector != 'None' \
    GROUP BY Sector \
    ORDER BY AVG(Volume) DESC;";
    
    data2 = db_class.executeAll(sql2)

    sect = [data['Sector'] for data in data2]
    volumes = [float(data['sector_volume']) for data in data2]

## 3. 섹터별 시가총액 차트 
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





    
    return render_template('index_sp.html', table1=table1,table2=table2,table3=table3,table4=table4, x_data=x_label, y_data=y_closed, x_data2=sect, y_data2=volumes, x_data3=sector,y_data3=capital)
