# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/13 下午1:33
# @filename: uuid_util
# @version : V1
# @description :

import uuid


def generate_uuid():
    return str(uuid.uuid4().hex)
