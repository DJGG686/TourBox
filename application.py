# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/4 下午9:13
# @filename: application
# @version : V1
# @description :

from flask import Flask, url_for, redirect

app = Flask(__name__)

app.config.from_pyfile('config/base_setting.py')


@app.route('/test')
def test():
    return redirect(url_for("user_api.getUserInfoBySearch", keyword="zyy"))


@app.route('/')
def mainPage():
    return '你好'

