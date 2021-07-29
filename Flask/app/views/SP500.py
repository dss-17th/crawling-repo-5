from flask import *
from app.modules import MysqlModule
from app import app
import pickle

@app.route('/SP500')
def sp():

    with open('datas/datas.pickle', 'rb') as f:
        (capital, sector, volumes, sect, y_closed, x_label, table4, table3, table2, table1) = pickle.load(f)

    
    return render_template('index_sp.html', table1=table1,table2=table2,table3=table3,table4=table4, x_data=x_label, y_data=y_closed, x_data2=sect, y_data2=volumes, x_data3=sector,y_data3=capital)
