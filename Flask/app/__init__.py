import pickle, os, datetime
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from flask import *
from app.config import Config # config 사용
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(TEMPLATES_AUTO_RELOAD=True, DEBUG=True,) 

#app을 생성하고 import, items에서 app객체를 import 받아 db연결 session을 생성하기 때문에
#from app.items.mongo_items import ArticleMongo, mongo_db 
#from app.items.mysql_items import ArticleMysql, mysql_db

#setting mongodb
#client_1 = {"username": "dss", "pw": "dsspw", "ip": "3.36.218.2"}
#app.config["MONGOALCHEMY_DATABASE"] = 'mongo' # mongo 라는 db를 사용
#app.config["MONGOALCHEMY_CONNECTION_STRING"] = f'mongodb://{client_1["username"]}:{client_1["pw"]}@{client_1["ip"]}:27017'
#mongo_db = MongoAlchemy(app)

#setting mysql
#client_2 = {"username": "root", "pw": "dss", "ip": "3.36.218.2"}
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{client_2["username"]}:{client_2["pw"]}@{client_2["ip"]}/dss'
#mysql_db = SQLAlchemy(app)

#class ArticleMysql(mysql_db.Model):

#    __tablename__ = 'article'

#     article_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
#     sentence = mysql_db.Column(mysql_db.String(500), nullable=False)
#     category = mysql_db.Column(mysql_db.String(20), nullable=False)

#     def __init__(self, sentence, category):
#         self.sentence = sentence
#         self.category = category

# mysql_db.create_all()

# class ArticleMongo(mongo_db.Document):
#     sentence = mongo_db.StringField()
#     category = mongo_db.StringField()
#     rdate = mongo_db.DateTimeField()


# with open('app/models/model.pkl', 'rb') as f:
#     model = pickle.load(f)

# @app.route("/")
# def index():
#     return render_template("index.html")

from app.views import AAPL, apis
from app.views import SP500

# @app.route("/predict")
# def predict():
#     result = {"code": 200}
#     sentence = request.values.get("sentence") # html에서 sentence의 value를 가져옴
#     print(sentence)
#     result["sentence"] = sentence

#     global model # 전역영역의 변수를 지역영역에서 사용하기 위해
#     result['datas'] = list(np.round(model.predict_proba([sentence])[0] * 100, 2))
#     result['categories'] = ['정치', '경제', '사회', '생활', '세계', 'IT']

#     category = result["categories"][model.predict([sentence])[0] - 100] # cate가 100부터이므로 0부터로 만들기 위해

#     # insert data into mongo_db
#     article = ArticleMongo(sentence=sentence, category=category, rdate=datetime.datetime.now())
#     article.save()

#     #insert data into mysql_db
#     global mysql_db
#     article = ArticleMysql(sentence=sentence, category=category)
#     mysql_db.session.add(article)
#     mysql_db.session.commit()

#     return jsonify(result)



app.run() # run.sh에서 flask run을 해서
