# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午2:05
# @filename: user
# @version : V1
# @description :
import random
import string
from dataclasses import dataclass, asdict
from typing import Optional
from enumeration.table_enum import Table
from database_connect.mysql_connector import MySQLConnector
from models import USER_SEARCH_CONTENT, ROUTE_PREVIEW_COLUMNS
from models.base_model import BaseModel
from models.model_factory import ModelFactory
from models.page_limit import Page
from util.file_util import delete_file, file_url
from util.sql_util import Condition


@dataclass
class User(BaseModel):
    db_connector = MySQLConnector()
    user_id: str = ""
    openid: str = ""
    nickname: str = ""
    avatar: str = ""
    gender: str = ""
    age: int = 0
    area: str = ""
    areacode: int = 0
    job: str = ""
    school: str = ""
    labelcode: int = 0
    signature: str = ""

    def __setattr__(self, key, value):
        if key == 'avatar' and value:
            super().__setattr__(key, file_url(key, value))
        else:
            super().__setattr__(key, value)

    def set_attr(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.keys:
                self.__setattr__(key, value)

    def get_user_info(self):
        return self.get_user_by_user_id(self.user_id)

    def get_user_by_user_id(self, user_id):
        result = self.db_connector.select(table=Table.user, where=Condition().equal('user_id', user_id), single=True)
        if result:
            self.set_attr(**result)
            return self.info
        else:
            return None

    @property
    def is_authenticated(self):
        return True

    def user_is_exist(self, user_id: Optional[str] = None):
        param = user_id if user_id else self.user_id
        if self.db_connector.select(table=Table.user, where=Condition().equal('user_id', param)):
            return True
        return False

    @staticmethod
    def create_user_nickname():
        return "用户" + ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def register(self):
        self.nickname = self.create_user_nickname()
        return self.db_connector.insert(table=Table.user, data=self.info)

    def update_avatar(self):
        result = self.db_connector.select(table=Table.user, columns=['avatar'],
                                          where=Condition().equal('user_id', self.user_id))
        if not result:
            return 'user not exist'
        if not self.db_connector.update(table=Table.user, data=dict(avatar=self.avatar),
                                        where=Condition().equal('user_id', self.user_id)):
            return 'avatar update failed'
        if result['avatar'] != 'default.jpeg':
            delete_file('avatar', result['avatar'])
        return None

    def search_user(self, keyword: str, page: Page):
        result = self.db_connector.select(table=Table.user,
                                          where=Condition().or_like(USER_SEARCH_CONTENT, keyword).page(page))
        return ModelFactory.change_list_to_model('user_preview', result)

    def update_user_info(self, data: dict = None):
        if not data:
            data = self.info
        if not self.db_connector.update(table=Table.user, data=data,
                                        where=Condition().equal('user_id', self.user_id)):
            return 'user update failed'
        return None

    def get_user_routes(self, page: Page, order: str = None, is_public: int = None):
        condition = Condition().equal(str(Table.user) + '.user_id', self.user_id).left_join(Table.user, 'user_id')
        if is_public is not None:
            condition.and_condition().equal('ispublic', is_public)
        if order:
            condition.decreasing(order)
        result = self.db_connector.select(table=Table.route, columns=ROUTE_PREVIEW_COLUMNS,
                                          where=condition.page(page))
        return ModelFactory.change_list_to_model('route_preview', result)

    def get_user_likes(self, page: Page):
        result = self.db_connector.select(table=Table.like,
                                          where=Condition().equal(str(Table.user) + '.user_id', self.user_id)
                                          .left_join(Table.route, 'route_id').left_join(Table.user, 'user_id')
                                          .decreasing(str(Table.like) + '.create_time').page(page))
        return ModelFactory.change_list_to_model('route_preview', result)

    def get_user_manage_routes(self, page: Page):
        result = self.db_connector.select(table=Table.manage,
                                          where=Condition().equal(str(Table.user) + '.user_id', self.user_id)
                                          .left_join(Table.route, 'route_id').left_join(Table.user, 'user_id')
                                          .page(page))
        return ModelFactory.change_list_to_model('route_preview', result)


if __name__ == '__main__':
    user = User(user_id='1082a0d7222fbd887837a216750e2d67')
    print('get_user_likes:', user.get_user_likes(Page(1, 10)))
    print('get_user_manage_routes:', user.get_user_manage_routes(Page(1, 10)))
    print('get_user_info:', user.get_user_info())
