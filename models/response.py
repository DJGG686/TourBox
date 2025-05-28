# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/11 下午1:33
# @filename: response
# @version : V1
# @description :
from typing import Union

from flask import Response, jsonify

from enumeration.status_code_enum import StatusCodeEnum
from models.base_model import BaseModel
from models.status import Status


class ApiResponse(BaseModel):
    def __init__(self, status: Status = Status(), data: Union[dict, list, str, None] = None):
        self.status: Status = status
        self.data: Union[dict, list, str, None] = data
        self.response: Response = self.init_response()

    def init_response(self) -> Response:
        res = self.status.info
        if self.data is not None:
            res.update({'data': self.data})
        return jsonify(res)

    def success(self) -> Response:
        self.response.status_code = StatusCodeEnum.SUCCESS.value
        return self.response

    def sql_error(self) -> Response:
        self.response.status_code = StatusCodeEnum.SQL_ERROR.value
        return self.response

    def miss_param(self) -> Response:
        self.response.status_code = StatusCodeEnum.MISSING_PARAMETER.value
        return self.response

    def not_found(self) -> Response:
        self.response.status_code = StatusCodeEnum.NOT_FOUND.value
        return self.response

    def upload_error(self) -> Response:
        self.response.status_code = StatusCodeEnum.UPLOAD_ERROR.value
        return self.response

    def authorization_failed(self) -> Response:
        self.response.status_code = StatusCodeEnum.AUTHORIZATION_FAILED.value
        return self.response

    def parameter_not_allowed(self) -> Response:
        self.response.status_code = StatusCodeEnum.PARAMETER_NOT_ALLOWED.value
        return self.response

    def code_invalid(self) -> Response:
        self.__init__(Status(StatusCodeEnum.CODE_INVALID, 'login failed'))
        self.response.status_code = StatusCodeEnum.CODE_INVALID.value
        return self.response

    def not_implemented(self):
        self.response.status_code = StatusCodeEnum.NOT_IMPLEMENTED.value
        return self.response

