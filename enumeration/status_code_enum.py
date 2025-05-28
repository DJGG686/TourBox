# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午1:19
# @filename: code_enum
# @version : V1
# @description : http接口返回状态码枚举

from enum import Enum


class StatusCodeEnum(Enum):
    SUCCESS = 200            # 请求成功
    SQL_ERROR = 201          # SQL错误
    MISSING_PARAMETER = 202  # 缺少参数
    NOT_FOUND = 203          # 未找到数据
    UPLOAD_ERROR = 204       # 上传文件错误
    AUTHORIZATION_FAILED = 205  # 认证失败
    PARAMETER_NOT_ALLOWED = 206    # 参数不允许
    PARAMETER_ERROR = 207    # 参数错误
    CODE_INVALID = 500       # code无效，code2Session请求失败
    NOT_IMPLEMENTED = 501    # 未实现

