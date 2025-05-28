# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/14 下午6:31
# @filename: user_preview
# @version : V1
# @description :
from dataclasses import dataclass

from models.base_model import BaseModel
from util.file_util import file_url


@dataclass
class UserPreview(BaseModel):
    user_id: str = ''
    nickname: str = ''
    avatar: str = ''
    signature: str = ''

    @property
    def info(self):
        self.avatar = file_url('avatar', self.avatar)
        return super().info


if __name__ == '__main__':
    user_preview1 = UserPreview(user_id='123456', nickname='digjie', avatar='avatar/123456.jpg',
                                signature='hello world')
    user_preview2 = UserPreview(user_id='654321', nickname='digjie2', avatar='avatar/654321.jpg',
                                signature='hello world2')
    l = [user_preview1.info, user_preview2.info]
    print(l)
