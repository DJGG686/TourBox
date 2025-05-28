from routeEdit import *


routes_api = Blueprint('routes_api', __name__)
routes_api.register_blueprint(route_edit, url_prefix='/edit')


@routes_api.route('/cover', methods=['POST'])
def postCover():
    route_id = request.values.get("route_id")
    if not route_id:
        return jsonify({'errmsg': 'Missing parameters: route_id', 'errcode': -2})
    if request.method == 'POST':
        # 接收图片
        cover = request.files.get('cover')
        # 未获取头像文件
        if not cover:
            return jsonify({'errmsg': 'missing cover', 'errcode': -2})
        cover_name = cover.filename
        # 保存图片到  ./static/cover
        filename = os.path.join(os.getcwd(), 'static/cover', cover_name)
        cover.save(filename)
        # 删除旧封面
        sql = "select cover from t_route where route_id = '{0}'".format(route_id)
        results = getOneFromDB(sql)
        # 更新封面图片
        result = update_image_to_db(cover_name, route_id, "update t_route set cover = %s where route_id = %s")
        if 'errmsg' in result:
            return jsonify(result)
        # 删除旧封面
        if results and 'errmsg' not in results:
            if results['cover'] != 'default.jpg':
                delete_filename = os.path.join(os.getcwd(), 'static/cover', results['cover'])
                delete_image(delete_filename)
        return jsonify(result)


@routes_api.route('/common', methods=['GET'])
def getCommonRoutes():
    _tag = request.values.get("tag")
    _order = request.values.get("order")
    if not _tag:
        return jsonify({'errmsg': 'missing tag', 'errcode': -1})
    if _tag == '0':
        _tag = 'ANY_VALUE(tag)'
    # 路线评分计算公式
    rubric = "((likenum*0.4)+(fork*0.3)+(round((lscore+rscore+tscore)/3, 1)*0.2)+(scoren*0.1)) pingfen"
    sql = '''
    select
    route_id,token,cover,avatar,u.nkname,title,descp,daynum,locnum,likenum,fork,round((lscore+rscore+tscore)/3, 1) as score,{0}
    from t_route t
    left join t_user u using(token)
    where tag = {1} limit 10;'''.format(rubric, _tag)
    # todo: 获取路线数量限制以及解决如何分组发送
    params = []
    if _order:
        sql = sql.rstrip(';')
        sql += " order by {0} desc;".format(_order)
    results = getAllFromDB(sql, params)
    if type(results) == list and results:
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
            r['cover'] = sendCover(r['cover'])
    return jsonify(results)


@routes_api.route('/selected', methods=['GET'])
def getSelectedRoutes():
    _tag = request.values.get("tag")
    _month = request.values.get("month")
    _year = request.values.get("year")
    if not _tag:
        return jsonify({'errmsg': 'missing parameters: tag', 'errcode': -2})
    params = []
    sql = '''
    select route_id,u.token,cover,avatar,u.nkname,title,descp,daynum,locnum,likenum,round((lscore+rscore+tscore)/3, 1) as score, reason
    from t_selec_route
    left join t_route r using(route_id)
    left join t_user u using(token)
    where r.tag = %s limit 10;'''
    if _tag == '0':
        sql = sql.replace('%s', 'ANY_VALUE(tag)')
    else:
        params.append(_tag)
    if _month and _year:
        sql = sql.replace('limit 10;', "and month(r.uptime)=%s and year(r.uptime)=%s limit 10;")
        params.append(_month)
        params.append(_year)
    results = getAllFromDB(sql, params)
    if type(results) == list and results:
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
            r['cover'] = sendCover(r['cover'])
    return jsonify(results)


@routes_api.route('/info', methods=['GET'])
def getRoutesInfo():
    route_id = request.values.get('route_id')
    if not route_id:
        return jsonify({'errmsg': 'missing route_id', 'errcode': -2})
    results = getRoute(route_id)
    if not results or "errmsg" in results:
        return jsonify(results)
    results['avatar'] = sendAvatar(results['avatar'])
    results['cover'] = sendCover(results['cover'])
    results['location'] = getLocationList(route_id)
    results['traffic'] = []
    results['way'] = []
    day = results['daynum']
    for i in range(day):
        traffic = getTrafficList(route_id, i)
        if 'errmsg' in traffic:
            return jsonify(traffic)
        results['traffic'].append(traffic)
        way = getWayList(route_id, i)
        if 'errmsg' in way:
            return jsonify(way)
        results['way'].append(way)
    sql = "select (max(longitude)+min(longitude))/2 longitude, (max(latitude)+min(latitude))/2 latitude from loca where route_id = '{0}';".format(route_id)
    coordinate = getOneFromDB(sql)
    if not coordinate or 'errmsg' in coordinate:
        return jsonify(coordinate)
    results['coordinate'] = coordinate
    return jsonify(results)


@routes_api.route('/search/<keyword>', methods=['GET'])
def getRoutesBySearch(keyword):
    words = keyword.split()
    data = []
    for word in words:
        sql = '''select
        route_id,cover,t.token,avatar,title,descp,daynum,locnum,likenum,round((lscore+rscore+tscore)/3, 1) as score
        from t_route t
        left join t_user u using(token)
        where title like '%{0}%' or descp like '%{0}%';
        '''.format(word)
        results = getAllFromDB(sql)
        if 'errmsg' in results:
            return jsonify(results)
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
            r['cover'] = sendCover(r['cover'])
        data.extend(results)
    return jsonify(sortByRelevance(data))

