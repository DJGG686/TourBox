# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/16 下午5:13
# @filename: traffic
# @version : V1
# @description :
from dataclasses import dataclass
from typing import Optional

from models.base_model import BaseModel


@dataclass
class Traffic(BaseModel):
    approach: Optional[str] = None
    begin: Optional[str] = None
    end: Optional[str] = None
    cost: Optional[str] = None
