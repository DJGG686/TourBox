# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午4:08
# @filename: www
# @version : V1
# @description : 注册蓝图，管理路由

from application import app
from controllers.user_controller import UserController
from controllers.route_controller import RouteController
from controllers.route_edit_controller import RouteEditController
from controllers.download_controller import download_api
from controllers.score_controller import ScoreController
from controllers.post_controller import PostController


user_controller = UserController()
route_controller = RouteController()
route_edit_controller = RouteEditController()
score_controller = ScoreController()
post_controller = PostController()


route_controller.blueprint.register_blueprint(route_edit_controller.blueprint, url_prefix='/edit')
app.register_blueprint(route_controller.blueprint, url_prefix='/routes')
app.register_blueprint(user_controller.blueprint, url_prefix='/user')
app.register_blueprint(download_api, url_prefix='/download')
app.register_blueprint(score_controller.blueprint, url_prefix='/score')
app.register_blueprint(post_controller.blueprint, url_prefix='/post')


