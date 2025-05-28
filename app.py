from flask import Flask, url_for, redirect
from routes import routes_api
from user import user_api
from download import download_api
from score import score_api
from post import post_api
from flasgger import Swagger
import yaml


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

app = Flask(__name__)
app.secret_key = 'lvxiaoku_nlzzd'
app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(routes_api, url_prefix='/routes')
app.register_blueprint(download_api, url_prefix='/download')
app.register_blueprint(score_api, url_prefix='/score')
app.register_blueprint(post_api, url_prefix='/post')
with open('swagger/api.yml', 'r', encoding='utf-8') as f:
    api_yaml = yaml.safe_load(f)
swagger = Swagger(app, config=swagger_config, template_file='swagger/api.yml')


@app.route('/test')
def test():
    return redirect(url_for("user_api.getUserInfoBySearch", keyword="zyy"))


@app.route('/')
def mainPage():
    return '你好'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
