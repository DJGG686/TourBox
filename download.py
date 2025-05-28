import os
from flask import Blueprint, send_from_directory, jsonify

download_api = Blueprint('download_api', __name__)


@download_api.route('/img/<path:path>', methods=['GET'])
def download_img(path):
    filename = os.path.join(os.getcwd(), 'static', path)
    if not os.path.exists(filename):
        return jsonify({'errmsg': 'img not found', 'errcode': -2})
    return send_from_directory(directory='static', path=path)
