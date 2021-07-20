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
    return render_template("index.html",data1=data1)