# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/29 上午11:16
# @filename: score_detail
# @version : V1
# @description :
from dataclasses import dataclass

from models.base_model import BaseModel
from util.file_util import file_url


@dataclass
class ScoreDetail(BaseModel):
    user_id: str = ''
    create_time: str = ''
    lscore: float = 0.0
    rscore: float = 0.0
    tscore: float = 0.0
    avatar: str = ''
    nickname: str = ''

    @property
    def info(self):
        self.avatar = file_url('avatar', self.avatar)
        return super().info
