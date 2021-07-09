from flask import *
from app.modules import MysqlModule
from app import app


@app.route("/<symbol>") 
def page(symbol):
    db_class= MysqlModule.Database()
 
    sql = f"SELECT * \
	FROM News \
	WHERE Symbol = '{symbol}';"
    data1 = db_class.executeAll(sql)
    
    sql = f"SELECT * \
	FROM daily \
	WHERE Symbol = '{symbol}';"
    data2 = db_class.executeAll(sql)

    line_xlabels = [data['Date'] for data in data2[:100]]
    line_data = [data['Close'] for data in data2[::-1][:100]]

    return render_template('index.html',data1=data1, data2=line_data, line_xlabels=line_xlabels)




