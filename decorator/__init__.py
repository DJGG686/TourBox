# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/13 下午12:42
# @filename: __init__.py
# @version : V1
# @description :
from util.data_check import check_location, check_way_point, check_traffic

PAGE_PARAMS = []

URL_PARAMS: dict = {
    'user': {
        'login': ['code'],
        'avatar': ['user_id', 'avatar'],
        'info': ['user_id'],
        'search': PAGE_PARAMS,
        'info/change': ['user_id'],
        'myroutes': ['user_id'] + PAGE_PARAMS,
        'mylikes': ['user_id'] + PAGE_PARAMS,
        'myposts': ['user_id'] + PAGE_PARAMS,
        'myjoins': ['user_id'] + PAGE_PARAMS,
        'mymanage': ['user_id']
    },
    'post': {
        'new': ['user_id', 'title', 'need'],
        'cover': ['post_id', 'cover'],
        'info': ['post_id'],
        'list': ['tag'] + PAGE_PARAMS,
        'search': PAGE_PARAMS,
        'join': ['post_id', 'user_id'],
        'quit': ['post_id', 'user_id'],
    },
    'route': {
        'cover': ['route_id', 'cover'],
        'explore': PAGE_PARAMS,
        'picked': PAGE_PARAMS,
        'info': ['route_id'],
        'search': PAGE_PARAMS,
    },
    'route_edit': {
        'new': ['user_id', 'title', 'description', 'ispublic', 'daynum', 'locnum', 'tag'],
        'update': ['route_id'],
        'location': ['route_id', 'data'],
        'way': ['route_id', 'data'],
        'traffic': ['route_id', 'data'],
        'manage': ['route_id', 'user_id'],
    },
    'score': {
        'route': ['route_id'] + PAGE_PARAMS,
        'users': ['route_id', 'user_id'],
    },
    'test': {
        'test': ['test']
    }
}

ALLOW_PARAMS = {
    'test': ['test'],
    'user': ['user_id', 'nickname', 'gender', 'age', 'area', 'areacode', 'job', 'school',
             'labelcode', 'signature'],
    'route': ['route_id', 'user_id', 'title', 'description', 'ispublic', 'day_num',
              'location_num', 'like_num', 'update_time', 'create_time', 'tag'],
    'score': ['route_id', 'user_id', 'lscore', 'rscore', 'tscore', 'create_time']
}

ORDER_TYPE = {
    'test': ['test'],
    'user': ['user_id', 'nickname', 'gender', 'age', 'area', 'areacode', 'job', 'school'],
    'route': ['day_num', 'location_num', 'like_num', 'update_time', 'create_time', 'score', 'lscore', 'rscore', 'tscore']
}

DATA_FORMAT = {
    'test': lambda x: print(x),
    'location': check_location,
    'way_point': check_way_point,
    'traffic': check_traffic
}

if __name__ == '__main__':
    for k, v in URL_PARAMS.items():
        print(k + ':')
        for k1, v1 in v.items():
            print('\t' + k1 + ':' + str(v1))
