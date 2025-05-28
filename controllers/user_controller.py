# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/4 下午9:06
# @filename: user_controller
# @version : V1
# @description :


from flask import Blueprint, Response
from decorator.param_filter import params_check
from logic.user_logic import UserLogic


class UserController:
    PREFIX = 'user'

    def __init__(self) -> None:
        self.logic = UserLogic()
        self.blueprint = Blueprint('user_api', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.blueprint.add_url_rule('/avatar', view_func=self.post_avatar, methods=['POST'])
        self.blueprint.add_url_rule('/info', view_func=self.get_user_info, methods=['GET'])
        self.blueprint.add_url_rule('/search/<keyword>', view_func=self.get_user_by_keyword, methods=['GET'])
        self.blueprint.add_url_rule('/info/change', view_func=self.change_user_info, methods=['PUT'])
        self.blueprint.add_url_rule('/myroutes', view_func=self.get_my_routes, methods=['GET'])
        self.blueprint.add_url_rule('/mylikes', view_func=self.get_my_likes, methods=['GET'])
        self.blueprint.add_url_rule('/myposts', view_func=self.get_my_posts, methods=['GET'])
        self.blueprint.add_url_rule('/myjoins', view_func=self.get_my_joins, methods=['GET'])
        self.blueprint.add_url_rule('/mymanage', view_func=self.get_my_manage, methods=['GET'])

    @params_check(prefix=PREFIX, url_rule='login')
    def login(self) -> Response:
        return self.logic.login()

    @params_check(prefix=PREFIX, url_rule='avatar')
    def post_avatar(self) -> Response:
        return self.logic.post_avatar()

    @params_check(prefix=PREFIX, url_rule='info')
    def get_user_info(self) -> Response:
        return self.logic.get_user_info()

    @params_check(prefix=PREFIX, url_rule='search')
    def get_user_by_keyword(self, keyword: str) -> Response:
        return self.logic.get_user_by_keyword(keyword)

    @params_check(prefix=PREFIX, url_rule='info/change')
    def change_user_info(self) -> Response:
        return self.logic.change_user_info()

    @params_check(prefix=PREFIX, url_rule='myroutes')
    def get_my_routes(self) -> Response:
        return self.logic.get_my_routes()

    @params_check(prefix=PREFIX, url_rule='mylikes')
    def get_my_likes(self) -> Response:
        return self.logic.get_my_likes()

    @params_check(prefix=PREFIX, url_rule='myposts')
    def get_my_posts(self) -> Response:
        return self.logic.get_my_posts()

    @params_check(prefix=PREFIX, url_rule='myjoins')
    def get_my_joins(self) -> Response:
        return self.logic.get_my_joins()

    @params_check(prefix=PREFIX, url_rule='mymanage')
    def get_my_manage(self) -> Response:
        return self.logic.get_my_manage()
