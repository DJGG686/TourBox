# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/8 下午6:16
# @filename: score_logic
# @version : V1
# @description :
from flask import request

from database_connect.mysql_connector import MySQLConnector
from decorator.authorization_filter import authorization
from decorator.param_filter import check_not_allow_params
from enumeration.table_enum import Table
from models.model_factory import ModelFactory
from models.page_limit import Page
from util.sql_util import Condition
from models.response import ApiResponse
from models.status import Status
from enumeration.status_code_enum import StatusCodeEnum as Code


class ScoreLogic:
    def __init__(self):
        self.db_connector = MySQLConnector()

    def get_route_score(self):
        route_id = request.values.get('route_id')
        if (result := self.db_connector.select(Table.score, columns=['score.*, nickname', 'avatar'],
                                               where=Condition().equal('route_id', route_id)
                                                       .left_join(Table.user, 'user_id').page(Page())
                                                       .order_by('score.create_time', 'DESC'))) is None:
            return ApiResponse(status=Status(code=Code.NOT_FOUND, msg='route not found')).not_found()
        return ApiResponse(data=ModelFactory.change_list_to_model('score_detail', result)).success()

    @authorization
    def get_user_score(self):
        route_id = request.values.get('route_id')
        user_id = request.values.get('user_id')
        if (result := self.db_connector.select(Table.score, columns=['score.*, nickname', 'avatar'],
                                               where=Condition().equal('route_id', route_id)
                                                       .and_condition().equal('user_id', user_id)
                                                       .left_join(Table.user, 'user_id').page(Page()),
                                               single=True)) is None:
            return ApiResponse(status=Status(code=Code.NOT_FOUND, msg='score not found')).not_found()
        return ApiResponse(data=ModelFactory.create_model('score_detail', **result)).success()

    @authorization
    @check_not_allow_params('score')
    def create_user_score(self):
        score = request.values.to_dict()
        if self.db_connector.insert(Table.score, score) is None:
            return ApiResponse(status=Status(code=Code.SQL_ERROR, msg='database error')).sql_error()
        return ApiResponse(data=ModelFactory.create_model('score_detail', **score)).success()

    @authorization
    @check_not_allow_params('score')
    def update_user_score(self):
        score = request.values.to_dict()
        if self.db_connector.update(Table.score, score,
                                    Condition().equal('route_id', score['route_id'])
                                    .and_condition().equal('user_id', score['user_id'])) is None:
            return ApiResponse(status=Status(code=Code.SQL_ERROR, msg='database error')).sql_error()
        return ApiResponse(data=ModelFactory.create_model('score_detail', **score)).success()

    @authorization
    def delete_user_score(self):
        return ApiResponse(status=Status(code=Code.NOT_IMPLEMENTED, msg='not implemented')).not_implemented()
