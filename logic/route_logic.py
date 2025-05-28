# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/8 下午6:15
# @filename: route_logic
# @version : V1
# @description :
from flask import jsonify, request

from decorator.authorization_filter import authorization
from enumeration.status_code_enum import StatusCodeEnum as code
from models.page_limit import Page
from models.response import ApiResponse
from models.route import Route
from models.status import Status
from util.file_util import generate_random_filename, save_file


class RouteLogic:
    def __init__(self):
        pass

    @authorization
    def post_cover(self):
        cover = request.files.get('cover')
        cover_filename = generate_random_filename(cover.filename)
        # save cover to server
        if not save_file('cover', cover, cover_filename):
            return ApiResponse(Status(code.UPLOAD_ERROR, 'upload failed')).upload_error()
        route = Route(route_id=request.values.get('route_id'), cover=cover_filename)
        if (msg := route.update_cover()) is not None:
            return ApiResponse(Status(code.SQL_ERROR, msg)).sql_error()
        return ApiResponse(Status(code.SUCCESS, 'upload success')).success()

    @staticmethod
    def get_explore_routes():
        tag = request.values.get('tag', 0, type=int)
        count = request.values.get('count', 10, type=int)
        if (data := Route().get_explore_routes(count, tag)) is not None:
            return ApiResponse(Status(code.SUCCESS, 'get explore routes success'), data=data).success()
        return ApiResponse(Status(code.SQL_ERROR, 'get explore routes failed')).sql_error()

    @staticmethod
    def get_picked_routes():
        tag = request.values.get('tag', 0, type=int)
        count = request.values.get('count', 10, type=int)
        if (data := Route().get_picked_routes(count, tag)) is not None:
            return ApiResponse(Status(code.SUCCESS, 'get picked routes success'), data=data).success()
        return ApiResponse(Status(code.SQL_ERROR, 'get picked routes failed')).sql_error()

    @staticmethod
    def get_route_info():
        route = Route(route_id=request.values.get('route_id'))
        if (data := route.get_route_info()) is not None:
            return ApiResponse(Status(code.SUCCESS, 'success'), data=data).success()
        return ApiResponse(Status(code.NOT_FOUND, 'route does not exist')).not_found()

    @staticmethod
    def get_routes_by_keyword(keyword):
        # keywords = keyword.split(' ')
        result = Route().search_routes(keyword, Page())
        return ApiResponse(Status(code.SUCCESS, 'search routes success'), data=result).success()
