from flask import *
from app.modules import MysqlModule
from app import app
import pickle

@app.route('/')
def index():    
    return redirect('/SP500') 
