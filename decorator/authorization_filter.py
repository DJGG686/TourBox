# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/13 下午12:44
# @filename: authorization_filter
# @version : V1
# @description :
from functools import wraps
from flask import request
from enumeration.status_code_enum import StatusCodeEnum
from enumeration.table_enum import Table
from models.response import ApiResponse
from models.status import Status
from util.sql_util import Condition
from util.token_util import verify_token
from database_connect.mysql_connector import MySQLConnector


def authorization(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return ApiResponse(Status(StatusCodeEnum.AUTHORIZATION_FAILED, 'Authorization token is missing')).authorization_failed()
        # 验证token
        payload, msg = verify_token(token)
        if msg:
            return ApiResponse(Status(StatusCodeEnum.AUTHORIZATION_FAILED, msg)).authorization_failed()
        return func(*args, **kwargs)

    return wrapper


def edit_permission(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        # 编辑权限检查
        payload, msg = verify_token(request.headers.get('Authorization'))
        # 获得用户可以编辑的route_id
        result = MySQLConnector().select(Table.route, columns=['route_id'],
                                         where=Condition().equal('user_id', payload['user_id']))
        route_ids = [route['route_id'] for route in result]
        # 判断用户是否有权限编辑当前route
        if int(request.values.get('route_id')) not in route_ids:
            return ApiResponse(Status(StatusCodeEnum.AUTHORIZATION_FAILED,
                                      'You do not have permission to edit this route')).authorization_failed()
        return func(*args, **kwargs)

    return wrapper

