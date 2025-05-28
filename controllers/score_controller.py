# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/5 下午11:03
# @filename: score_controller
# @version : V1
# @description :

from flask import Blueprint, request

from decorator.param_filter import params_check
from logic.score_logic import ScoreLogic


class ScoreController:
    PREFIX = 'score'

    def __init__(self):
        self.logic = ScoreLogic()
        self.blueprint = Blueprint('demo_score', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/route', view_func=self.get_route_score, methods=['GET'])
        self.blueprint.add_url_rule('/users', view_func=self.user_score_control,
                                    methods=['GET', 'POST', 'PUT', 'DELETE'])

    @params_check(prefix=PREFIX, url_rule='/route')
    def get_route_score(self):
        return self.logic.get_route_score()

    @params_check(prefix=PREFIX, url_rule='/users')
    def user_score_control(self):
        if request.method == 'GET':
            return self.logic.get_user_score()
        elif request.method == 'POST':
            return self.logic.create_user_score()
        elif request.method == 'PUT':
            return self.logic.update_user_score()
        elif request.method == 'DELETE':
            return self.logic.delete_user_score()
