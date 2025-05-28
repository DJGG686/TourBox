import pymysql
from config import db_info


# 定义数据库连接的上下文管理器
class DBConnection:
    def __init__(self, database_info=None):
        if database_info is None:
            database_info = db_info
        self.host = database_info["host"]
        self.user = database_info["user"]
        self.password = database_info["password"]
        self.database = database_info["database"]

    def __enter__(self):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, charset='utf8', cursorclass=pymysql.cursors.DictCursor, database=self.database)
        self.cursor = self.db.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.cursor.close()
        self.db.close()
        return True
