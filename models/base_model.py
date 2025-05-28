# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/16 下午4:23
# @filename: base_model
# @version : V1
# @description :
from dataclasses import dataclass


@dataclass
class BaseModel:

    @property
    def info(self):
        return self.__dict__

    def __str__(self):
        return str(self.info)

    @property
    def keys(self):
        return self.__dict__.keys()
