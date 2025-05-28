# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/5 下午11:04
# @filename: post_controller
# @version : V1
# @description :

from flask import request, Blueprint, jsonify
from logic.post_logic import PostLogic


class PostController:
    def __init__(self):
        self.post_logic = PostLogic()
        self.blueprint = Blueprint('post', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/new', view_func=self.create_new_post, methods=['POST'])
        self.blueprint.add_url_rule('/cover', view_func=self.post_cover, methods=['POST'])
        self.blueprint.add_url_rule('/info', view_func=self.get_post_info, methods=['GET'])
        self.blueprint.add_url_rule('/list', view_func=self.get_post_list, methods=['GET'])
        self.blueprint.add_url_rule('/search/<string:keyword>', view_func=self.get_posts_by_keyword, methods=['GET'])
        self.blueprint.add_url_rule('/join', view_func=self.join_post, methods=['POST'])
        self.blueprint.add_url_rule('/quit', view_func=self.quit_post, methods=['POST'])

    @staticmethod
    def create_new_post():
        return jsonify('create new post')

    @staticmethod
    def post_cover():
        return jsonify('post cover')

    @staticmethod
    def get_post_info(self):
        return jsonify('get post info')

    @staticmethod
    def get_post_list(self):
        return jsonify('get post list')

    @staticmethod
    def get_posts_by_keyword(self, keyword):
        return jsonify('get posts by keyword')

    @staticmethod
    def join_post():
        return jsonify('join post')

    @staticmethod
    def quit_post():
        return jsonify('quit post')
