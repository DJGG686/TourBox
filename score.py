from flask import request, Blueprint, url_for
from tools import *

score_api = Blueprint('demo_score', __name__)


def get_score(route_id, token=None):
    if not token:
        sql = "select token,nkname,avatar,CAST(uptime AS CHAR) uptime,lscore,rscore,tscore from score s left join t_user u using(token) where route_id=%s;"
        params = (route_id,)
    else:
        sql = "select token,nkname,avatar,CAST(uptime AS CHAR) uptime,lscore,rscore,tscore from score s left join t_user u using(token) where route_id=%s and u.token=%s;"
        params = (route_id, token)
    return getAllFromDB(sql, params)


@score_api.route('/route', methods=['GET'])
def getRoutesScores():
    route_id = request.values.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'Missing parameters: route_id', 'errcode': -2})
    results = get_score(route_id)
    print(results)
    if type(results) == list and results:
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
    return jsonify(results)


@score_api.route('/users', methods=['POST', 'GET', 'PUT'])
def userScoreController():
    route_id = request.values.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'Missing parameters: route_id', 'errcode': -2})
    _token = request.values.get("token")
    # 缺少token参数
    if not _token:
        return jsonify({'errmsg': 'Missing parameters: token', 'errcode': -2})
    if request.method == 'POST':
        _lscore = request.values.get('lscore')
        _rscore = request.values.get('rscore')
        _tscore = request.values.get('tscore')
        if not _lscore or not _rscore or not _tscore:
            return jsonify({'errmsg': 'Missing parameters: lscore or rscore or tscore', 'errcode': -2})
        # 插入score关系表
        sql = '''insert into score (route_id,token,uptime,lscore,rscore,tscore)
        values (%s,%s,curdate(),%s,%s,%s)'''
        params = (route_id, _token, _lscore, _rscore, _tscore)
        result = updateToDB(sql, params)
        if 'errmsg' in result:
            return jsonify(result)
        # 更新t_route表得分
        sql2 = '''update t_route set 
        lscore=(lscore*scoren+%s)/(scoren+1),rscore=(rscore*scoren+%s)/(scoren+1),tscore=(tscore*scoren+%s)/(scoren+1),scoren=scoren+1
        where route_id=%s;'''
        params2 = (_lscore, _rscore, _tscore, route_id)
        result = updateToDB(sql2, params2)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'Score submitted success'})
    elif request.method == 'GET':
        return jsonify(get_score(route_id, _token))
    elif request.method == 'PUT':
        _lscore = request.values.get('lscore')
        _rscore = request.values.get('rscore')
        _tscore = request.values.get('tscore')
        if not _lscore or not _rscore or not _tscore:
            return jsonify({'errmsg': 'Missing parameters: lscore or rscore or tscore', 'errcode': -2})
        results = get_score(route_id, token=_token)
        if not results or 'errmsg' in results:
            return jsonify(results)
        diff_lscore = float(_lscore) - float(results['lscore'])
        diff_rscore = float(_rscore) - float(results['rscore'])
        diff_tscore = float(_tscore) - float(results['tscore'])
        sql = '''update score set lscore=%s,rscore=%s,tscore=%s where route_id=%s and token=%s'''
        params = (_lscore, _rscore, _tscore, route_id, _token)
        result = updateToDB(sql, params)
        if 'errmsg' in result:
            return jsonify(result)
        sql = '''update t_route set 
        lscore=(lscore*scoren+%s)/scoren,rscore=(rscore*scoren+%s)/scoren,tscore=(tscore*scoren+%s)/scoren
        where route_id=%s;'''
        params = (diff_lscore, diff_rscore, diff_tscore, route_id)
        result = updateToDB(sql, params)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'Score updated success'})
