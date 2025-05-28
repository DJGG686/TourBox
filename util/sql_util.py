# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/14 上午11:58
# @filename: sql_util
# @version : V1
# @description :
from models.page_limit import Page


class Condition:
    def __init__(self, no_where=False):
        self.sql = f"WHERE" if not no_where else ""

    def equal(self, column, value=None, any_value=None):
        if any_value:
            self.sql += f" {column} = ANY({any_value})"
        else:
            self.sql += f" {column} = '{value}'"
        return self

    def not_equal(self, column, value):
        self.sql += f" {column} <> '{value}'"
        return self

    def greater_than(self, column, value):
        self.sql += f" {column} > '{value}'"
        return self

    def less_than(self, column, value):
        self.sql += f" {column} < '{value}'"
        return self

    def greater_than_or_equal(self, column, value):
        self.sql += f" {column} >= '{value}'"
        return self

    def less_than_or_equal(self, column, value):
        self.sql += f" {column} <= '{value}'"
        return self

    def like(self, column, value):
        self.sql += f" {column} LIKE '%{value}%'"
        return self

    def or_like(self, columns, value):
        self.sql += ' OR'.join([f" {column} LIKE '%{value}%'" for column in columns])
        return self

    def not_like(self, column, value):
        self.sql += f" {column} NOT LIKE '%{value}%'"
        return self

    def in_list(self, column, value_list):
        self.sql += f" {column} IN ({','.join(value_list)})"
        return self

    def not_in_list(self, column, value_list):
        self.sql += f" {column} NOT IN ({','.join(value_list)})"
        return self

    def and_condition(self):
        self.sql += f" AND"
        return self

    def or_condition(self):
        self.sql += f" OR"
        return self

    def page(self, page: Page):
        self.sql += f" LIMIT {page.page_size * (page.page - 1)}, {page.page_size}"
        return self

    def limit(self, limit):
        self.sql += f" LIMIT {limit}"
        return self

    def left_join(self, table, on_condition):
        self.sql = f"LEFT JOIN {table} USING({on_condition}) " + self.sql
        return self

    def order_by(self, column, order=None):
        self.sql += f" ORDER BY {column} {order if order else ''}"
        return self

    def decreasing(self, column):
        self.sql += f" ORDER BY {column} DESC"
        return self

    def increasing(self, column):
        self.sql += f" ORDER BY {column} ASC"
        return self

    def __str__(self):
        return self.sql

    def to_sql(self):
        return self.sql


if __name__ == '__main__':
    condition = Condition()
    condition.equal('id', 1).and_condition().equal('name', 'test')
    print(condition)

    search_content = ['nickname', 'signature', 'area', 'job', 'school']
    print(Condition().or_like(search_content, 'test'))
