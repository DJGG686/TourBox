# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/5 下午11:01
# @filename: route_edit_controller
# @version : V1
# @description :

from flask import Blueprint, request

from decorator.param_filter import params_check
from logic.route_edit_logic import RouteEditLogic


class RouteEditController:
    PREFIX = 'route_edit'

    def __init__(self):
        self.logic = RouteEditLogic()
        self.blueprint = Blueprint('route_edit', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/new', view_func=self.create_new_route, methods=['POST'])
        self.blueprint.add_url_rule('/update', view_func=self.update_route_info, methods=['PUT', 'DELETE'])
        self.blueprint.add_url_rule('/location', view_func=self.edit_location, methods=['POST', 'PUT', 'DELETE'])
        self.blueprint.add_url_rule('/way', view_func=self.edit_way, methods=['POST', 'PUT', 'DELETE'])
        self.blueprint.add_url_rule('/traffic', view_func=self.edit_traffic, methods=['POST', 'PUT', 'DELETE'])
        self.blueprint.add_url_rule('/manage', view_func=self.manage_route, methods=['POST'])

    @params_check(prefix=PREFIX, url_rule='/new')
    def create_new_route(self):
        return self.logic.create_new_route()

    @params_check(prefix=PREFIX, url_rule='/update')
    def update_route_info(self):
        if request.method == 'PUT':
            return self.logic.update_route_info()
        elif request.method == 'DELETE':
            return self.logic.delete_route()

    @params_check(prefix=PREFIX, url_rule='/location')
    def edit_location(self):
        if request.method == 'POST':
            return self.logic.add_location()
        elif request.method == 'PUT':
            return self.logic.update_location()
        elif request.method == 'DELETE':
            return self.logic.delete_location()

    @params_check(prefix=PREFIX, url_rule='/way')
    def edit_way(self):
        if request.method == 'POST':
            return self.logic.add_way()
        elif request.method == 'PUT':
            return self.logic.update_way()

    @params_check(prefix=PREFIX, url_rule='/traffic')
    def edit_traffic(self):
        if request.method == 'POST':
            return self.logic.add_traffic()
        elif request.method == 'PUT':
            return self.logic.update_traffic()

    @params_check(prefix=PREFIX, url_rule='/manage')
    def manage_route(self):
        return self.logic.manage_route()