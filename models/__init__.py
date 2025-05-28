# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午1:56
# @filename: __init__.py
# @version : V1
# @description :


USER_SEARCH_CONTENT = ['nickname', 'signature', 'area', 'job', 'school']
ROUTE_SEARCH_CONTENT = ['title', 'description', 'city', 'name', 'address']
USER_PREVIEW_COLUMNS = ['user_id', 'nickname', 'avatar', 'signature']

ROUTE_PREVIEW_COLUMNS = ['route_id', 'title', 'user.user_id', 'nickname', 'cover', 'avatar', 'day_num',
                         'like_num', 'location_num', 'round((lscore+rscore+tscore)/3, 1) as score']
