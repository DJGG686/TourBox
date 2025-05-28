# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/8 下午6:15
# @filename: user_logic
# @version : V1
# @description :
import requests
from flask import Response, jsonify, request

from decorator.authorization_filter import authorization
from decorator.param_filter import check_not_allow_params, check_order_type
from enumeration.status_code_enum import StatusCodeEnum as code
from models.page_limit import Page
from models.response import ApiResponse
from models.status import Status
from models.user import User
from util import generate_user_id
from util.file_util import save_file, generate_random_filename
from util.token_util import generate_token
from util.wx_api_util import wx_login


class UserLogic:
    def __init__(self):
        pass

    @staticmethod
    def login() -> Response:
        _code = request.values.get('code')
        # 调用微信登录接口
        result = wx_login(_code)
        # 验证code, 微信登录结果
        if 'errcode' in result or 'session_key' not in result and 'openid' not in result:
            return ApiResponse().code_invalid()
        # 保存用户信息
        user_id = generate_user_id(result['openid'])
        token = generate_token(result['session_key'])
        user = User(user_id=user_id, openid=result['openid'])
        if not user.user_is_exist():
            if user.register() is None:
                return ApiResponse().code_invalid()
        return ApiResponse(Status(code.SUCCESS, 'login success'),
                           data=dict(user_id=user_id, token=token)).success()

    @authorization
    def post_avatar(self) -> Response:
        avatar = request.files.get('avatar')
        avatar_filename = generate_random_filename(avatar.filename)
        # 保存用户头像文件
        if not save_file('avatar', avatar, avatar_filename):
            return ApiResponse(Status(code.UPLOAD_ERROR, 'upload failed')).upload_error()
        user = User(user_id=request.values.get('user_id'), avatar=avatar_filename)
        # 更新用户头像
        if (msg := user.update_avatar()) is not None:
            return ApiResponse(Status(code.SQL_ERROR, msg)).sql_error()
        return ApiResponse(Status(code.SUCCESS, 'upload success')).success()

    @authorization
    def get_user_info(self) -> Response:
        user = User(user_id=request.values.get('user_id'))
        if (data := user.get_user_info()) is not None:
            return ApiResponse(Status(code.SUCCESS, 'success'), data=data).success()
        return ApiResponse(Status(code.NOT_FOUND, 'user not exist')).not_found()

    @staticmethod
    def get_user_by_keyword(keyword: str) -> Response:
        # keywords = keyword.split(' ')
        result = User().search_user(keyword, Page())
        return ApiResponse(Status(code.SUCCESS, 'search users success'), data=result).success()

    @authorization
    @check_not_allow_params('user')
    def change_user_info(self) -> Response:
        data = dict(request.values)
        user = User(**data)
        if msg := user.update_user_info(data):
            return ApiResponse(Status(code.SQL_ERROR, msg)).sql_error()
        return ApiResponse(Status(code.SUCCESS, 'change user info success')).success()

    @check_order_type('route')
    def get_my_routes(self) -> Response:
        user_id = request.values.get('user_id')
        user = User(user_id=user_id)
        if (data := user.get_user_routes(Page(), request.values.get('order'), request.values.get('ispublic'))) is not None:
            return ApiResponse(Status(code.SUCCESS, 'get my routes success'), data=data).success()
        return ApiResponse(Status(code.SQL_ERROR, 'failed')).sql_error()

    @staticmethod
    def get_my_likes() -> Response:
        user = User(user_id=request.values.get('user_id'))
        if (data := user.get_user_likes(Page())) is not None:
            return ApiResponse(Status(code.SUCCESS, 'get my likes success'), data=data).success()
        return ApiResponse(Status(code.SQL_ERROR, 'failed')).sql_error()

    @staticmethod
    def get_my_posts() -> Response:
        return jsonify("get_my_posts")

    @staticmethod
    def get_my_joins() -> Response:
        return jsonify("get_my_joins")

    @staticmethod
    def get_my_manage() -> Response:
        user = User(user_id=request.values.get('user_id'))
        if (data := user.get_user_manage_routes(Page())) is not None:
            return ApiResponse(Status(code.SUCCESS, 'get my manage success'), data=data).success()
        return ApiResponse(Status(code.SQL_ERROR, 'failed')).sql_error()
