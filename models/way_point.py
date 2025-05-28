# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/16 下午4:20
# @filename: way_point
# @version : V1
# @description :
from dataclasses import dataclass
from typing import Optional

from models.location import Location


@dataclass
class WayPoint(Location):
    round_time: Optional[str] = None


if __name__ == '__main__':
    wp = WayPoint(latitude=39.984094, longitude=116.319236, name='北京大学', address='北京市海淀区中关村南大街10号', route_time='20min')
    print(wp)
