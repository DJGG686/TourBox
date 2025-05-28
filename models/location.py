# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午3:14
# @filename: location
# @version : V1
# @description :

from dataclasses import dataclass
from typing import Optional
from models.base_model import BaseModel


@dataclass
class Location(BaseModel):
    """location"""
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


if __name__ == '__main__':
    location = Location(address='北京市朝阳区阜通东大街10号', latitude=39.921556, longitude=116.407113, name='北京市朝阳区阜通东大街10号')
    print(location.info)

