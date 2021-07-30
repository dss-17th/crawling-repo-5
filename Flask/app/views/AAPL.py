from flask import *
from app.modules import MysqlModule
from app import app
import pandas as pd

@app.route("/<symbol>")
def page(symbol):
    db_class= MysqlModule.Database()
    symbol = symbol.upper()
    if symbol == 'SP500' :
        return redirect('/SP500')
    sql = f"SELECT * \
	FROM News \
	WHERE Symbol = '{symbol}';"
    data1 = db_class.executeAll(sql)
    datafile = pd.read_csv('Symbol.csv')
    name = datafile[datafile['Symbol'] == symbol]['Name'].values[0]
    sector = datafile[datafile['Symbol'] == symbol]['Sector'].values[0]
    industry = datafile[datafile['Symbol'] == symbol]['Industry'].values[0]
    lat = datafile[datafile['Symbol'] == symbol]['lat'].values[0]
    lng = datafile[datafile['Symbol'] == symbol]['lng'].values[0]
    color = datafile[datafile['Symbol'] == symbol]['color1'].values[0]
    return render_template("index.html",data1=data1, symbol=symbol, name=name, sector=sector, industry=industry, lat=lat, lng=lng, color=color)