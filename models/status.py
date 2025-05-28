# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午2:52
# @filename: status
# @version : V1
# @description :
from typing import Union
from enumeration.status_code_enum import StatusCodeEnum
from models.base_model import BaseModel


class Status(BaseModel):
    def __init__(self, code: Union[int, StatusCodeEnum] = StatusCodeEnum.SUCCESS, msg: str = 'success'):
        self.code: StatusCodeEnum = StatusCodeEnum(code)
        self.msg: str = msg

    @property
    def info(self):
        return dict(code=self.code.value, msg=self.msg)

