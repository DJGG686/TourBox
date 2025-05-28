import traceback
from typing import Optional

import pymysql
import os
import sys
from config.local_setting import DB_INFO
from util.sql_util import Condition

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MySQLConnector:
    # 数据库连接器单例模式
    __connector = None

    def __new__(cls, *args, **kwargs):
        if not cls.__connector:
            cls.__connector = super(MySQLConnector, cls).__new__(cls, *args, **kwargs)
        return cls.__connector

    def __init__(self):
        try:
            self.__connection = pymysql.connect(**DB_INFO, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)
        # 新建游标
        self.__cursor = self.__connection.cursor()
        self.set_autocommit(True)

    def __enter__(self):
        return self

    def __del__(self):
        if self.__connection:
            self.__connection.commit()
            self.__connection.close()
            self.__cursor.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()

    def commit(self):
        self.__connection.commit()

    def np_exception_handle(self, func, *args, **kwargs):
        """
        函数执行异常处理器。捕获func执行过程中出现的异常, 如果发生异常，则回滚数据库连接，
        并打印异常信息，返回None;
        正常执行func时，返回func的执行结果。
        :param func: 需要执行的函数
        :type func: function
        :param args: 函数的参数
        :type args: tuple, list
        :param kwargs: 函数的关键字参数
        :type kwargs: dict
        :return: func的执行结果，如果func执行过程中出现异常，则返回None
        :rtype: any
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.rollback()
            traceback.print_exc()
            print(f"Error executing query: {e}")
            return None

    def check_and_reconnect(self):
        """
        检查数据库连接是否断开，如果断开，则重新连接数据库
        :return: None
        :rtype:
        """
        try:
            self.__connection.ping(reconnect=True)
        except pymysql.Error:
            self.__connection = pymysql.connect(**DB_INFO, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.__cursor = self.__connection.cursor()

    def set_autocommit(self, autocommit):
        """
        设置数据库连接为自动提交或非自动提交
        :param autocommit: True 将连接设置为自动提交，False 将连接设置为非自动提交
        :type autocommit: bool
        :return: None
        :rtype:
        """
        self.__connection.autocommit(autocommit)

    def fetch_all(self, query, params=None):
        """
        执行查询语句，并返回所有结果， 用于查询多条数据
        :param query: sql查询语句
        :type query: str
        :param params: 查询语句参数
        :type params: tuple, list
        :return: 查询结果，如果查询失败，则返回None
        :rtype: dict, None
        """
        def _execute_query():
            self.check_and_reconnect()
            self.__cursor.execute(query, params)
            result = self.__cursor.fetchall()
            return result

        return self.np_exception_handle(_execute_query)

    def fetch_one(self, query, params=None):
        def _execute_query():
            self.check_and_reconnect()
            self.__cursor.execute(query, params)
            result = self.__cursor.fetchone()
            return result

        return self.np_exception_handle(_execute_query)

    def execute(self, query, params=None):
        """
        执行非查询语句，用于增删改操作
        :param query: sql语句
        :type query: str
        :param params: sql语句参数
        :type params: tuple, list
        :return: 受影响的行数，如果执行失败，则返回None
        :rtype: int, None
        """

        def _execute_query():
            self.check_and_reconnect()
            self.__cursor.execute(query, params)
            return self.__cursor.rowcount

        return self.np_exception_handle(_execute_query)

    def get_last_insert_id(self):
        result = self.fetch_one("SELECT LAST_INSERT_ID() as id")
        return result['id'] if result else None

    def select(self, table, columns: Optional[list] = None, where: Optional[str | Condition] = None, single: bool = False):
        select_sql = f"SELECT {','.join(columns) if columns else '*'} FROM {table} {str(where) if where else ''}"
        print(select_sql)
        return self.fetch_one(select_sql) if single else self.fetch_all(select_sql)

    def update(self, table, data: dict, where: Optional[str | Condition] = None):
        update_sql = f"UPDATE {table} SET {','.join([f'{k}=%s' for k in data.keys()])} {str(where) if where else ''}"
        return self.execute(update_sql, tuple(data.values()))

    def insert(self, table, data: dict):
        insert_sql = f"INSERT INTO {table} ({','.join(data.keys())}) VALUES ({','.join(['%s' for _ in data.keys()])})"
        return self.execute(insert_sql, tuple(data.values()))

    def delete(self, table, to_delete=None, where: Optional[str | Condition] = None):
        delete_sql = f"DELETE {to_delete if to_delete else ''} FROM {table} {str(where) if where else ''}"
        return self.execute(delete_sql)


if __name__ == '__main__':
    with MySQLConnector() as db:
        a = db.select('route')
        print(a[0]['create_time'])
