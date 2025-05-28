import hmac
import os
import traceback
from flask import jsonify, url_for
from dbconnect import *


def get_db_connection():
    db = pymysql.connect(host='localhost', user='root', password='dj124342', charset='utf8', cursorclass=pymysql.cursors.DictCursor, database='demo')
    return db


# 使用加盐和openid和session_key等方式哈希作为key，然后session_key作为value
def generate_token(key, value):
    return hmac.new(key.encode('utf-8'), value.encode('utf-8'), 'MD5').hexdigest()


def get_openid_by_token(token):
    # 根据token获取openid
    sql = "select openid from t_user where token = '{0}';".format(token)
    results = getOneFromDB(sql)
    if not results or 'errmsg' in results:
        return None
    return results['openid']


def user_verify(_openid, _token):
    # 1.openid,session_key,token都在数据库中,返回token和openid
    # 2.openid在数据库中,session_key更新了,生成新的token更新到数据库,返回token和openid
    # 3.openid,session_key,token都不在数据库中,相当于注册用户,将数据插入数据库
    # 4.数据库查询失败
    sql = "select token from t_user where openid = '{0}';".format(_openid)
    results = getOneFromDB(sql)
    if not results:
        return 3
    if 'errmsg' in results:
        return 4
    v_token = results['token']
    if v_token == _token:
        return 1
    else:
        return 2


def update_image_to_db(filename, _token, sql):
    args = (filename, _token)
    result = updateToDB(sql, args)
    if 'errmsg' in result:
        return result
    return {"msg": "update success"}


def delete_image(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return "delete success"
    except Exception as e:
        traceback.print_exc()
        return "delete fail"


def sortByRelevance(list_before_sort):
    to_sort = []
    result = []
    # 计算相关度count
    for i in list_before_sort:
        if [i, list_before_sort.count(i)] not in to_sort:
            to_sort.append([i, list_before_sort.count(i)])
    # 排序
    to_sort.sort(key=lambda x: (x[1]), reverse=True)
    # 剔除隐藏相关度值
    for [route, num] in to_sort:
        result.append(route)
    return result


def getRoute(route_id):
    sql = "select r.*,u.nkname,u.avatar from t_route r left join t_user u using(token) where route_id={0};".format(route_id)
    return getOneFromDB(sql)


def getLocationList(route_id):
    sql = "select max(list)+1 num from loca where route_id = {0};"
    num = getOneFromDB(sql.format(route_id))['num']
    print(num)
    results = []
    for i in range(num):
        sql = "select name,address,longitude,latitude from loca where route_id = {0} and list = {1};".format(route_id, i)
        locations = getAllFromDB(sql)
        results.append(locations)
    return results


def getInsertLocationSql(route_id, datas):
    sql = "insert into loca (route_id,list,name,address,longitude,latitude) values "
    for i in range(len(datas)):  # 遍历list,i+1代表list序号
        for j in range(len(datas[i])):  # 遍历list[i]中每一个地点信息
            data = datas[i][j]
            miss = ""
            values = "{0},{1}".format(route_id, i)
            for key in ['name', 'address', 'longitude', 'latitude']:
                if key not in data:
                    miss += " " + key
                else:
                    if key == 'name' or key == 'address':
                        values += ",'{0}'".format(data.get(key))
                    else:
                        values += ",{0}".format(data.get(key))
            sql += "({0}),".format(values)
            if miss:
                return {'errmsg': "missing params:data[{0}][{1}]".format(i, j) + miss, 'errcode': -2}
    sql = sql.rstrip(',') + ";"
    return sql


def insertLocation(route_id, datas):
    sql = getInsertLocationSql(route_id, datas)
    if 'errmsg' in sql:
        return sql
    result = updateToDB(sql)
    if 'errmsg' in result:
        return result
    updateToDB("update t_route set locnum = {0} where route_id = {1};".format(result['msg'], route_id))
    return {'msg': 'insert new locations success'}


def getWayList(route_id, day):
    sql = "select name,address,longitude,latitude,round_time from way where route_id = {0} and dy = {1} order by way_id;".format(route_id, day)
    data = getAllFromDB(sql)
    return data


def getInsertWaySql(route_id, datas):
    sql = "insert into way (route_id,dy,name,address,longitude,latitude,round_time) values "
    for i in range(len(datas)):
        for j in range(len(datas[i])):
            way = datas[i][j]
            miss = ""
            values = "{0},{1}".format(route_id, i)
            for key in ["name", "address", "longitude", "latitude", "round_time"]:
                if key not in way:
                    miss += " " + key
                else:
                    if key == "longitude" or key == "latitude":
                        values += ",{0}".format(way.get(key))
                    else:
                        values += ",'{0}'".format(way.get(key))
            if miss:
                return {'errmsg': 'missing params: data[{0}][{1}] '.format(i, j) + miss, 'errcode': -2}
            sql += "({0}),".format(values)
    sql = sql.rstrip(',') + ";"
    return sql


def insertWay(route_id, datas):
    days = len(datas)
    update_days_sql = "update t_route set daynum = {0} where route_id = {1};".format(days, route_id)
    result = updateToDB(update_days_sql)
    if 'errmsg' in result:
        return result
    sql = getInsertWaySql(route_id, datas)
    if 'errmsg' in sql:
        return sql
    result = updateToDB(sql)
    if 'errmsg' in result:
        return result
    return {'msg': 'insert new way success'}


def getTrafficList(route_id, day):
    select_sql = "select max(num)+1 nums from traf where route_id = {0} and dy = {1};".format(route_id, day)
    nums = int(getOneFromDB(select_sql)['nums'])
    if not nums:
        return []
    data = []
    for i in range(nums):
        sql = "select approach,line,start,ed,tme from traf where route_id = {0} and dy = {1} and num = {2};".format(route_id, day, i)
        traffic = getAllFromDB(sql)
        data.append(traffic)
    return data


def insertTraffic(route_id, datas):
    sql = getInsertTrafficSql(route_id, datas)
    if 'errmsg' in sql:
        return sql
    result = updateToDB(sql)
    if 'errmsg' in result:
        return result
    return {'msg': 'insert new traffic success'}


def getInsertTrafficSql(route_id, datas):
    sql = "insert into traf (route_id,dy,num,approach,line,start,ed,tme) values "
    for i in range(len(datas)):
        for j in range(len(datas[i])):
            traffic = datas[i][j]
            for k in range(len(traffic)):
                line = traffic[k]
                miss = ""
                values = "{0},{1},{2}".format(route_id, i, j)
                for key in ["approach", "line", "start", "end", "time"]:
                    if key not in line:
                        miss += " " + key
                    else:
                        if key == "approach" or key == "time":
                            values += ",{0}".format(line.get(key))
                        else:
                            values += ",'{0}'".format(line.get(key))
                if miss:
                    return {'errmsg': 'missing params: data[{0}][{1}][{2}] '.format(i, j, k) + miss, 'errcode': -2}
                sql += "({0}),".format(values)
    sql = sql.rstrip(',') + ";"
    return sql


def findStartNode(nodes):
    start_nodes = set()
    end_nodes = set()
    for start, end in nodes:
        start_nodes.add(start)
        end_nodes.add(end)
    begin = start_nodes - end_nodes
    if len(begin) == 1:
        return begin.pop()
    else:
        return None


def sendCover(_path):
    if _path:
        return url_for('download_api.download_img', _external=True, path='cover/' + _path)
    else:
        return url_for('download_api.download_img', _external=True, path='cover/default.jpeg')


def sendAvatar(_path):
    if _path:
        return url_for('download_api.download_img', _external=True, path='avatar/' + _path)
    else:
        return url_for('download_api.download_img', _external=True, path='avatar/default.jpeg')


def getOneFromDB(sql, args=None):
    empty = {}
    try:
        with DBConnection() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchone()
            if not results:
                return empty
            return results
    except pymysql.Error as e:
        traceback.print_exc()
        print(e.args[0], e.args[1])
        return {'errmsg': 'Database query failed', 'errcode': e.args[0]}


def updateToDB(sql, args=None):
    try:
        with DBConnection() as cursor:
            result = cursor.execute(sql, args)
            if result == 0:
                return {'errmsg': 'Database query failed: not found', 'errcode': -1}
            return {'msg': result}
    except pymysql.Error as e:
        traceback.print_exc()
        print(e.args[0], e.args[1])
        return {'errmsg': 'Database query failed', 'errcode': e.args[0]}


def getAllFromDB(sql, args=None):
    empty = []
    try:
        with DBConnection() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchall()
            if not results:
                return empty
            return results
    except pymysql.Error as e:
        traceback.print_exc()
        print(e.args[0], e.args[1])
        return {'errmsg': 'Database query failed', 'errcode': e.args[0]}


def deleteAndUpdate(sql, sql2, params=None, params2=None):
    # 用于执行两种操作需同时执行的情况
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.execute(sql2, params2)
        # result = cursor.rowcount 是insert语句，返回插入了多少数据，用于更新某些值
        db.commit()
        return result
    except pymysql.Error as e:
        db.rollback()
        traceback.print_exc()
        return {'errmsg': 'Database query failed', 'errcode': e.args[0]}
    finally:
        cursor.close()
        db.close()


