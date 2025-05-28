# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/15 上午10:58
# @filename: table_enum
# @version : V1
# @description :

from enum import Enum


class Table(Enum):
    """
    表名枚举类
    """
    user = 'user'
    route = 'route'
    like = 'like'
    location = 'location'
    manage = 'manage'
    member = 'member'
    polyline = 'polyline'
    post = 'post'
    score = 'score'
    tag = 'tag'
    traffic = 'traffic'
    way_list = 'way_list'
    user_preview = 'user_preview'
    base_cities = 'base_cities'
    picked = 'picked'

    def __str__(self):
        return f'`{self.value}`'


if __name__ == '__main__':
    print(Table.user)
    print(Table.user.value)
