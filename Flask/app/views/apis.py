from flask import *
from app.modules import MysqlModule
from app import app
import pandas as pd

@app.route("/data/<symbol>") 
def data(symbol):
    result = {'code': 200}
    db_class= MysqlModule.Database()
    try : 
        term = request.values.get('term')
        if term == 'week':
            sql = f"SELECT date_format(daily.Date, '%%Y-%%m-%%d') as Date, Close \
            FROM US_Stock.daily \
            WHERE Symbol = '{symbol}'\
            order by DATE DESC\
            LIMIT 6;"
        elif term == 'month':
            sql = f"SELECT date_format(daily.Date, '%%Y-%%m-%%d') as Date, Close \
            FROM US_Stock.daily \
            WHERE Symbol = '{symbol}'\
            order by DATE DESC\
            LIMIT 22;"
        elif term == 'month3':
            sql = f"SELECT date_format(daily.Date, '%%Y-%%m-%%d') as Date, Close \
            FROM US_Stock.daily \
            WHERE Symbol = '{symbol}'\
            order by DATE DESC\
            LIMIT 64;"
        elif term == 'year':
            sql = f"SELECT date_format(daily.Date, '%%y-%%m-%%d') as Date, Close \
            FROM US_Stock.daily \
            WHERE Symbol = '{symbol}'\
            order by DATE DESC\
            LIMIT 260;"
        data2 = db_class.executeAll(sql)[::-1]
        result['data2'] = data2
    except : 
        pass

    try : 
        value = request.values.get('value')
        datafile = pd.read_csv('symbol.csv')
        valuedata = datafile[datafile['Symbol'] == symbol][value].values[0]
        print(valuedata)
        sql = f"SELECT market_capitalization, company.Symbol \
                FROM US_Stock.company, US_Stock.daily \
                WHERE US_Stock.company.Symbol = US_Stock.daily.Symbol and {value} = '{valuedata}' \
                ORDER BY daily.Date desc, market_capitalization DESC LIMIT 100;"
        datas = db_class.executeAll(sql)
        sames = set()
        for data in datas:
            sames.add(data['Symbol'])
            if len(sames) >= 5:
                break
        data3 = []
        for same in sames:
            same_value = []
            for data in datas:
                if data['Symbol'] == same:
                    same_value.append(data['market_capitalization'])
                    if len(same_value) == 2:
                        data['market_capitalization'] = round(((same_value[0] - same_value[1]) / same_value[1]) * 100, 2)
                        data3.append(data)
                        break        
        result['data3'] = data3[::-1]
    except : 
        pass    
    
    try : 
        value_1 = request.values.get('value_1')
        sql_1 = f"SELECT date_format(Company_low.update_date,'%%Y-%%m-%%d') as update_date, profit\
                FROM US_Stock.Company_low \
                WHERE Company_low.Symbol ='{symbol}'\
                ORDER BY Company_low.update_date ASC;"
        datas_1 = db_class.executeAll(sql_1)
        result['datas_1'] = datas_1
    except : 
        pass

    try : 
        value_2 = request.values.get('value_2')
        sql_2 = f"SELECT date_format(Company_low.update_date,'%%Y-%%m-%%d') as update_date, real_profit\
	            FROM US_Stock.Company_low\
                WHERE Company_low.Symbol = '{symbol}'\
                ORDER BY Company_low.update_date ASC;"
        datas_2 = db_class.executeAll(sql_2)
        result['datas_2'] = datas_2
    except : 
        pass



    return jsonify(result)