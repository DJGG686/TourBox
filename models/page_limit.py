# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/15 下午7:09
# @filename: page_limit
# @version : V1
# @description :
from flask import request


class Page:
    def __init__(self, page=None, page_size=None):
        if page is None or page_size is None:
            self.page = request.values.get('page', 1, type=int)
            self.page_size = request.values.get('pageSize', 10, type=int)
        else:
            self.page = page
            self.page_size = page_size
