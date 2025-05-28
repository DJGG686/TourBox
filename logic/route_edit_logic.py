# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/8 下午6:16
# @filename: route_edit_logic
# @version : V1
# @description :
from typing import Dict, Union

from flask import jsonify, request
from decorator.authorization_filter import authorization, edit_permission
from decorator.param_filter import check_not_allow_params, check_data_format
from enumeration.status_code_enum import StatusCodeEnum as Code
from models.response import ApiResponse
from models.route import Route
from models.status import Status
from util.data_check import check_location, check_way_point


class RouteEditLogic:

    @authorization
    @edit_permission
    @check_not_allow_params('route')
    def create_new_route(self):
        # 初始化参数
        kwargs: Dict[str, Union[str, list[int]]] = request.values.to_dict()
        kwargs['tag'] = [int(tag) for tag in request.form.getlist('tag')]
        route = Route(**kwargs)
        # 插入数据库
        result = route.insert_route()
        if isinstance(result, str):
            return ApiResponse(Status(Code.SQL_ERROR, result)).sql_error()
        return ApiResponse(Status(Code.SUCCESS, 'create new route success'), data=result).success()

    @authorization
    @edit_permission
    @check_not_allow_params('route')
    def update_route_info(self):
        # 初始化参数
        kwargs = request.values.to_dict()
        tags = None
        if 'tag' in kwargs:
            tags = [int(tag) for tag in request.form.getlist('tag')]
            kwargs.pop('tag')
        route = Route(**kwargs)
        # 更新route信息
        ret = route.update_route(kwargs)
        if len(ret) == 2:
            if ret[1] == 0:
                return ApiResponse(Status(Code.SUCCESS, 'route info not change')).success()
        else:
            return ApiResponse(Status(Code.SQL_ERROR, ret)).sql_error()
        # 更新tag信息
        if tags is not None:
            if (msg := route.update_tags(tags)) is not None:
                return ApiResponse(Status(Code.SQL_ERROR, msg)).sql_error()
        return ApiResponse(Status(Code.SUCCESS, 'update route info success')).success()

    @authorization
    @edit_permission
    def delete_route(self):
        # 根据id删除
        route_id = request.values.get('route_id')
        if (msg := Route(route_id=route_id).delete_route()) is not None:
            return ApiResponse(Status(Code.SQL_ERROR, msg)).sql_error()
        return ApiResponse(Status(Code.SUCCESS, 'delete route success')).success()
    
    @authorization
    @edit_permission
    @check_data_format('location')
    def add_location(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).add_location(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'add location success')).success()

    @authorization
    @edit_permission
    @check_data_format('location')
    def update_location(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).update_location(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'update location success')).success()

    @authorization
    @edit_permission
    def delete_location(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).delete_location(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'delete location success')).success()

    @authorization
    @edit_permission
    @check_data_format('way_point')
    def add_way(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).add_way(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'add way success')).success()

    @authorization
    @edit_permission
    @check_data_format('way_point')
    def update_way(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).update_way(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'add way success')).success()

    @authorization
    @edit_permission
    @check_data_format('traffic')
    def add_traffic(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).add_traffic(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'add traffic success')).success()

    @authorization
    @edit_permission
    @check_data_format('traffic')
    def update_traffic(self):
        route_id = request.json.get('route_id')
        if (msg := Route(route_id=route_id).update_traffic(request.json.get('data'))) is not None:
            return jsonify(Status(Code.SQL_ERROR, msg).info)
        return ApiResponse(Status(Code.SUCCESS, 'update traffic success')).success()

    @authorization
    @edit_permission
    def manage_route(self):
        return jsonify('manage route')
