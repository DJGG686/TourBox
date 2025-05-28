# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/13 下午12:22
# @filename: file_util
# @version : V1
# @description :

import os
import traceback

from flask import url_for

from config.production_setting import BASE_URL
from util.uuid_util import generate_uuid


def generate_random_filename(filename):
    return generate_uuid() + os.path.splitext(filename)[-1]


def save_file(file_type, content, name) -> bool:
    file_name = os.path.join(os.getcwd(), f'static/{file_type}', name)
    try:
        content.save(file_name)
        print(f'{name} saved successfully.')
        return True
    except Exception as e:
        traceback.print_exc()
        print(e)
        print(f'{name} save failed.')
        return False


def delete_file(file_type, filename):
    delete_filename = os.path.join(os.getcwd(), f'static/{file_type}', filename)
    try:
        if os.path.exists(delete_filename):
            os.remove(delete_filename)
            print(f'{filename} deleted successfully.')
    except Exception as e:
        traceback.print_exc()
        print(e)
        print(f'{filename} delete failed.')


def file_url(file_type, filename):
    return f'{BASE_URL}/download/img/{file_type}/{filename}'


def set_avatar_and_cover_url(data: dict):
    data['avatar'] = file_url('avatar', data['avatar'] if data['avatar'] else 'default.jpeg')
    data['cover'] = file_url('cover', data['cover'] if data['cover'] else 'default.jpeg')
    return data

