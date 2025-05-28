# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/16 下午4:34
# @filename: route_preview
# @version : V1
# @description :
from dataclasses import dataclass
from typing import Optional

from models.base_model import BaseModel
from util.file_util import set_avatar_and_cover_url


@dataclass
class RoutePreview(BaseModel):
    route_id: Optional[int] = None
    title: str = ''
    cover: str = ''
    user_id: str = ''
    nickname: str = ''
    avatar: str = ''
    day_num: int = 0
    location_num: int = 0
    like_num: int = 0
    score: float = 0.0

    @property
    def info(self):
        return set_avatar_and_cover_url(super().info)


@dataclass
class PickedRoutePreview(RoutePreview):
    reason: str = ''


if __name__ == '__main__':
    route_1 = RoutePreview(route_id=1, title='测试路线1', cover='bd_logo1.png', user_id='123456', nickname='测试用户1', avatar='bd_logo1.png', day_num=10, location_num=10, like_num=100, score=8.5)
    print(route_1.info)

