from flask import request, Blueprint
from tools import *
from datetime import datetime

post_api = Blueprint('post_api', __name__)


# todo: 增加图片上传功能
@post_api.route('/new', methods=['POST'])
def createNewPost():
    _token = request.values.get('token')
    if not _token:
        return jsonify({'errmsg': 'missing parameters: token', 'errcode': -2})
    data = request.values.to_dict()
    data.pop('token')
    keys = ""
    values = ""
    params = []
    for key, value in data.items():
        params.append(value)
        keys = keys + ",{0}".format(key)
        values = values + ",%s".format(value)
    current_time = datetime.now().strftime('%Y-%m-%d')
    sql = "insert into t_post (token,uptime{2}) values ('{0}','{1}'{3})".format(_token, current_time, keys, values)
    result = updateToDB(sql, params)
    if 'errmsg' in result:
        return jsonify(result)
    sql = "select post_id from t_post where token='{0}' and uptime='{1}'".format(_token, current_time)
    results = getOneFromDB(sql)
    if not results or 'errmsg' in results:
        return jsonify(results)
    return jsonify({'msg': 'create new route success', 'post_id': results['post_id']})


@post_api.route('/info', methods=['GET'])
def getPostInfo():
    post_id = request.values.get('post_id')
    sql = "select * from t_post where post_id={0}".format(post_id)
    results = getOneFromDB(sql)
    if not results or 'errmsg' in results:
        print(results)
        return jsonify(results)
    # 获取拼团leader信息
    token = results['token']
    sql = "select token,nkname,signature,avatar from t_user where token='{0}'".format(token)
    leader_info = getOneFromDB(sql)
    if not leader_info or 'errmsg' in leader_info:
        return jsonify(leader_info)
    leader_info['avatar'] = sendAvatar(leader_info['avatar'])
    results['leader'] = leader_info
    results.pop('token')
    # 获取路线信息
    route_id = results['route_id']
    if route_id:
        rubric = "((likenum*0.4)+(fork*0.3)+(round((lscore+rscore+tscore)/3, 1)*0.2)+(scoren*0.1)) pingfen"
        sql = '''select
        route_id,token,title,cover,avatar,descp,daynum,locnum,likenum,fork,round((lscore+rscore+tscore)/3, 1) as score,{0}
        from t_route t
        left join t_user u using(token)
        where route_id={1};'''.format(rubric, route_id)
        route_info = getOneFromDB(sql)
        if not route_info or 'errmsg' in route_info:
            return jsonify(results)
        route_info['cover'] = sendCover(route_info['cover'])
        route_info['avatar'] = sendCover(route_info['avatar'])
        results['route'] = route_info
        results.pop('route_id')
    # 获取成员信息
    sql = "select name,token,avatar,signature,wechat,phone from members left join t_user using(token) where post_id={0};"
    members = getAllFromDB(sql.format(post_id))
    if not members or 'errmsg' in members:
        return jsonify(members)
    for r in members:
        r['avatar'] = sendCover(r['avatar'])
    results['members'] = members
    _token = request.values.get('token')
    if _token:
        sql = "select name,token,avatar,signature,wechat,phone from members left join t_user using(token) where post_id={0} and token='{1}';".format(post_id, _token)
        my_info = getOneFromDB(sql)
        if my_info:
            results['my_info'] = my_info
    return jsonify(results)


@post_api.route('/list', methods=['GET'])
def getPostList():
    _tag = request.values.get("tag")
    if not _tag:
        return jsonify({'errmsg': 'missing parameters: tag', 'errcode': -1})
    if _tag == '0':
        _tag = 'ANY_VALUE(tag)'
    sql = '''select post_id,p.title,CAST(endtime AS CHAR) endtime,p.descp,need,num,cover
from t_post p
left join t_route r using(route_id)
where tag={0} limit 10;'''.format(_tag)
    results = getAllFromDB(sql)
    if not results or 'errmsg' in results:
        return jsonify(results)
    for r in results:
        r['cover'] = sendCover(r['cover'])
    return jsonify(results)


@post_api.route('/search/<string:keyword>', methods=['GET'])
def getPostsByKeyword(keyword):
    words = keyword.split()
    data = []
    for word in words:
        sql = '''select
        post_id,p.title,CAST(endtime AS CHAR) endtime,p.descp,need,num,cover
        from t_post p
        left join t_route r using(route_id)
        where r.title like '%{0}%' or r.descp like '%{0}%' or p.title like '%{0}%' or p.descp like '%{0}%';
        '''.format(word)
        results = getAllFromDB(sql)
        if not results or 'errmsg' in results:
            return jsonify(results)
        for r in results:
            r['cover'] = sendCover(r['cover'])
        data.extend(results)
    return jsonify(sortByRelevance(data))


@post_api.route('/join', methods=['POST'])
def joinPost():
    data = request.values.to_dict()
    miss = ""
    keys = ""
    values = ""
    params = []
    # 验证参数完整性
    for key in ['post_id', 'token', 'name', 'wechat', 'phone']:
        if key not in data:
            miss = miss + key + " "
        else:
            keys = keys + "{0},".format(key)
            values = values + "%s,".format(data[key])
            params.append(data[key])
    if miss:
        return jsonify({'errmsg': 'missing parameters: {0}'.format(miss), 'errcode': -2})
    keys = keys.rstrip(',')
    values = values.rstrip(',')
    post_id = data['post_id']
    # 加入成员信息并更新post帖子已参团人数
    sql = "update t_post set num=num+1 where post_id={0}".format(post_id)
    sql2 = "insert into members ({0}) values ({1});".format(keys, values)
    result = deleteAndUpdate(sql, sql2, params2=params)
    if type(result) == dict:
        return jsonify(result)
    return jsonify({'msg': 'join post success'})


@post_api.route('/quit', methods=['POST'])
def quitPost():
    token = request.values.get('token')
    if not token:
        return jsonify({'errmsg': 'missing parameters: token', 'errcode': -2})
    post_id = request.values.get('post_id')
    if not post_id:
        return jsonify({'errmsg': 'missing parameters: post_id', 'errcode': -2})
    # 删除成员信息并更新post帖子已参团人数
    sql = "delete from members where post_id={0} and token='{1}';".format(post_id, token)
    sql2 = "update t_post set num=num-1 where post_id={0}".format(post_id)
    result = deleteAndUpdate(sql, sql2)
    if type(result) == dict:
        return jsonify(result)
    return jsonify({'msg': 'quit post success'})



