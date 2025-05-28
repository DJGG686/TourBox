from flask import Blueprint, request
from tools import *
from datetime import datetime

route_edit = Blueprint('route_create', __name__)


@route_edit.route('/new', methods=['POST'])
def createNewRoute():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'Missing parameters: token', 'errcode': -2})
    data = dict(request.values)
    data.pop('token')
    keys = ""
    values = ""
    params = []
    for key, value in data.items():
        print("{0}:{1},".format(key, value))
        params.append(value)
        keys = keys + ",{0}".format(key)
        values = values + ",%s".format(value)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "insert into t_route (token,uptime,author{2}) values ('{0}','{1}','{0}'{3})".format(_token, current_time, keys, values)
    result = updateToDB(sql, params)
    if 'errmsg' in result:
        return jsonify(result)
    sql = "select route_id from t_route where token='{0}' and uptime='{1}'".format(_token, current_time)
    results = getOneFromDB(sql)
    if not results or 'errmsg' in results:
        return jsonify(results)
    return jsonify({'msg': 'create new route success', 'route_id': results['route_id']})


@route_edit.route('/update', methods=['PUT', 'DELETE'])
def updateRouteInfo():
    route_id = request.values.get("route_id")
    if not route_id:
        return jsonify({'errmsg': 'missing token', 'errcode': -2})
    if request.method == 'PUT':
        data = dict(request.values)
        data.pop('route_id')
        keys = ""
        params = []
        # 拼接sql update语句
        for key, value in data.items():
            print("{0}={1},".format(key, value))
            params.append(value)
            keys = keys + "{0}=%s,".format(key)
        keys = keys.rstrip(',')
        sql = "update t_route set {1} where route_id = '{0}'".format(route_id, keys)
        result = updateToDB(sql, params)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'update data success', 'route_id': route_id})
    else:
        sql = "delete from t_route where route_id = '{0}'".format(route_id)
        result = updateToDB(sql)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'delete data success'})


@route_edit.route('/location', methods=['POST', 'PUT', 'DELETE'])
def editLocation():
    route_id = request.json.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'Missing params: route_id', 'errcode': -2})
    datas = request.json.get('data')
    if not datas:
        return jsonify({'errmsg': 'Missing params: data', 'errcode': -2})
    if request.method == 'POST':
        # 插入地点列表数据
        return jsonify(insertLocation(route_id, datas))
    elif request.method == 'DELETE':
        to_delete = ""
        for data in datas:
            to_delete += "'{0}',".format(data)
        to_delete = to_delete.rstrip(',')
        sql = "delete from loca where route_id={0} and name in ({1})".format(route_id, to_delete)
        print(sql)
        result = updateToDB(sql)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'delete data success'})
    else:
        sql = "delete from loca where route_id={0}".format(route_id)
        sql2 = getInsertLocationSql(route_id, datas)
        if "errmsg" in sql2:
            return jsonify(sql2)
        location_num = deleteAndUpdate(sql, sql2)
        if type(location_num) == dict:
            return jsonify(location_num)
        # 更新location_num
        update_location_num_sql = "update t_route set locanum = {0} where route_id = {1};".format(location_num, route_id)
        result = updateToDB(update_location_num_sql)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'update data success'})


@route_edit.route('/way', methods=['POST', 'PUT'])
def editWay():
    route_id = request.json.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'missing param: route_id', 'errcode': -2})
    datas = request.json.get('data')
    if not datas:
        return jsonify({'errmsg': 'missing params: data', 'errcode': -2})
    if request.method == 'POST':
        # 插入路线数据
        return jsonify(insertWay(route_id, datas))
    elif request.method == 'PUT':
        # 先删除原有的数据，再插入新数据
        sql = "delete from way where route_id={0}".format(route_id)
        sql2 = getInsertWaySql(route_id, datas)
        if "errmsg" in sql2:
            return jsonify(sql2)
        result = deleteAndUpdate(sql, sql2)
        if type(result) == dict:
            return jsonify(result)
        # 更新天数
        days = len(datas)
        update_days_sql = "update t_route set daynum = {0} where route_id = {1};".format(days, route_id)
        result = updateToDB(update_days_sql)
        if 'errmsg' in result:
            return jsonify(result)
        return jsonify({'msg': 'update data success'})


@route_edit.route('/traffic', methods=['POST', 'PUT'])
def editTraffic():
    route_id = request.json.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'missing param: route_id', 'errcode': -2})
    datas = request.json.get('data')
    if not datas:
        return jsonify({'errmsg': 'missing params: data', 'errcode': -2})
    if request.method == 'POST':
        # 插入交通数据
        return jsonify(insertTraffic(route_id, datas))
    else:
        # 先删除原有的数据，再插入新数据
        sql = "delete from traf where route_id={0}".format(route_id)
        sql2 = getInsertTrafficSql(route_id, datas)
        if "errmsg" in sql2:
            return jsonify(sql2)
        result = deleteAndUpdate(sql, sql2)
        if type(result) == dict:
            return jsonify(result)
        return jsonify({'msg': 'update data success'})
