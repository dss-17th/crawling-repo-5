import pymysql
from app.modules import user
class Database():
    def __init__(self):
        self.db = pymysql.connect(host=user.host,
                                  user=user.user,
                                  password=user.pw,
                                  db=user.db,
                                  charset='utf8')

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args)  
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit():
        self.db.commit()