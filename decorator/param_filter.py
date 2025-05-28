# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/11 下午6:31
# @filename: param_filter
# @version : V1
# @description :
from functools import wraps
from flask import request, jsonify
from decorator import URL_PARAMS, ALLOW_PARAMS, ORDER_TYPE, DATA_FORMAT
from enumeration.status_code_enum import StatusCodeEnum as Code
from models.response import ApiResponse
from models.status import Status


def params_check(prefix: str = 'test', url_rule: str = 'test'):
    params_list = URL_PARAMS.get(prefix, {}).get(url_rule, [])

    def decorator(func):
        @wraps(wrapped=func)
        def wrapper(*args, **kwargs):
            params = request.values.to_dict()
            files = request.files.to_dict()
            missing_params = []
            print('参数如下：', params, files)
            for param in params_list:
                if param not in params and param not in files:
                    missing_params.append(param)
            if missing_params:
                missing_params = ', '.join(missing_params)
                response = ApiResponse(status=Status(Code.MISSING_PARAMETER, f'Missing parameters: {missing_params}'))
                return response.miss_param()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_not_allow_params(prefix: str = 'test'):
    params_list = ALLOW_PARAMS.get(prefix, [])

    def decorator(func):
        @wraps(wrapped=func)
        def wrapper(*args, **kwargs):
            params = request.values.to_dict()
            for param in params:
                if param not in params_list:
                    response = ApiResponse(Status(Code.PARAMETER_NOT_ALLOWED, f'Not allow parameter: {param}'))
                    return response.parameter_not_allowed()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_order_type(prefix: str = 'test'):
    order_type_list = ORDER_TYPE.get(prefix, [])

    def decorator(func):
        @wraps(wrapped=func)
        def wrapper(*args, **kwargs):
            order = request.values.get('order')
            if order and order not in order_type_list:
                return ApiResponse(
                    Status(Code.PARAMETER_NOT_ALLOWED, f'Order type is illegal: {order}')).parameter_not_allowed()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_data_format(prefix: str = 'test'):
    check_func = DATA_FORMAT.get(prefix, None)

    def decorator(func):
        @wraps(wrapped=func)
        def wrapper(*args, **kwargs):
            data = request.json.get('data')
            if check_func and not check_func(data):
                return jsonify(Status(Code.PARAMETER_ERROR, 'data format error').info)
            return func(*args, **kwargs)

        return wrapper

    return decorator
