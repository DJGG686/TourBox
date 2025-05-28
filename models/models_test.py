# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午2:10
# @filename: models_test
# @version : V1
# @description :
import json

from models.user import User
from models.status import Status
from enumeration.status_code_enum import StatusCodeEnum

user = User()
user.get_user_by_user_id("02e9b7825255b5f93b968a0532734eba")
print(user)

print(user.is_authenticated)
print(user.data)

status = Status(StatusCodeEnum.SUCCESS, "test status")
result = status.data
result["data"] = user.data
print(result)

