# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/11 下午9:10
# @filename: token_util
# @version : V1
# @description :
import time
from typing import Optional

import jwt
from jwt import exceptions
from config.production_setting import JWT_SECRET_KEY, JWT_TOKEN_EXPIRES


def generate_token(user_id):
    """
    Generate JWT token for user authentication.
    :param user_id: User ID
    :type user_id: str
    :return: JWT token
    :rtype: str
    """
    _now = int(time.time())
    payload = {
        'exp': _now + JWT_TOKEN_EXPIRES,
        'iat': _now,
        'user_id': user_id
    }
    print(payload)
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')


def verify_token(token):
    """
    Verify JWT token for user authentication.
    :param token: JWT token
    :type token: str
    :return: payload or None and error message or None
    :rtype: dict or None, str or None
    """
    payload = None
    msg = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
    except exceptions.ExpiredSignatureError:
        msg = 'Token expired, please login again.'
    except jwt.DecodeError:
        msg = 'Token decoding failed.'
    except jwt.InvalidTokenError:
        msg = 'Invalid token.'
    return payload, msg


if __name__ == '__main__':
    _token = generate_token('02e9b7825255b5f93b968a0532734eba')
    print(_token)
    time.sleep(3)
    _user_id = verify_token(_token)
    print(_user_id)
