# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/11 下午10:11
# @filename: wx_api_util
# @version : V1
# @description :
import requests

from config.production_setting import WX_LOGIN_API, APPID, SECRET


def wx_login(code: str) -> dict:
    req_params = {
        'appid': APPID,
        'secret': SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    return requests.get(WX_LOGIN_API, params=req_params).json()
