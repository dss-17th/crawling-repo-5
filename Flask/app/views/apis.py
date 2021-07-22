from flask import *
from app.modules import MysqlModule
from app import app


@app.route("/data/<symbol>") 
def data(symbol):
    result = {'code': 200}
    term = request.values.get('term')
    


    db_class= MysqlModule.Database()

    sql = f"SELECT * \
	FROM News \
	WHERE Symbol = '{symbol}';"
    data1 = db_class.executeAll(sql)
    
    if term == 'week':
        sql = f"SELECT * \
        FROM US_Stock.daily \
        WHERE Symbol = '{symbol}'\
        order by DATE DESC\
        LIMIT 6;"
    elif term == 'month':
        sql = f"SELECT * \
        FROM US_Stock.daily \
        WHERE Symbol = '{symbol}'\
        order by DATE DESC\
        LIMIT 22;"
    elif term == 'month3':
        sql = f"SELECT * \
        FROM US_Stock.daily \
        WHERE Symbol = '{symbol}'\
        order by DATE DESC\
        LIMIT 64;"
    elif term == 'year':
        sql = f"SELECT * \
        FROM US_Stock.daily \
        WHERE Symbol = '{symbol}'\
        order by DATE DESC\
        LIMIT 260;"
    
    data2 = db_class.executeAll(sql)[::-1]
    
    result['term'] = term
    result['symbol'] = symbol
    result['data2'] = data2
    return jsonify(result)