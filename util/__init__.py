# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/11 下午8:48
# @filename: __init__.py
# @version : V1
# @description :
import hmac


def generate_user_id(key):
    return hmac.new(key.encode('utf-8'), digestmod='MD5').hexdigest()


if __name__ == '__main__':
    _key = 'oL1BS5KiwSdUMtlNRX4ToxTDb_DM'
    print(generate_user_id(_key))
