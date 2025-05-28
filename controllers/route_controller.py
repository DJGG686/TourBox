# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/5 下午10:59
# @filename: route_controller
# @version : V1
# @description :


from flask import Blueprint, Response
from decorator.param_filter import params_check
from logic.route_logic import RouteLogic


class RouteController:
    PREFIX = 'route'

    def __init__(self):
        self.route_logic = RouteLogic()
        self.blueprint = Blueprint('routes', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/cover', view_func=self.post_cover, methods=['POST'])
        self.blueprint.add_url_rule('/explore', view_func=self.get_explore_routes, methods=['GET'])
        self.blueprint.add_url_rule('/picked', view_func=self.get_picked_routes, methods=['GET'])
        self.blueprint.add_url_rule('/info', view_func=self.get_route_info, methods=['GET'])
        self.blueprint.add_url_rule('/search/<keyword>', view_func=self.get_routes_by_keyword, methods=['GET'])

    @params_check(prefix=PREFIX, url_rule='cover')
    def post_cover(self) -> Response:
        return self.route_logic.post_cover()

    @params_check(prefix=PREFIX, url_rule='explore')
    def get_explore_routes(self) -> Response:
        return self.route_logic.get_explore_routes()

    @params_check(prefix=PREFIX, url_rule='picked')
    def get_picked_routes(self) -> Response:
        return self.route_logic.get_picked_routes()

    @params_check(prefix=PREFIX, url_rule='info')
    def get_route_info(self) -> Response:
        return self.route_logic.get_route_info()

    @params_check(prefix=PREFIX, url_rule='search/<keyword>')
    def get_routes_by_keyword(self, keyword: str) -> Response:
        return self.route_logic.get_routes_by_keyword(keyword)
