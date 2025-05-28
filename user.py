import string
import random
import requests
from flask import request, redirect, Blueprint
from tools import *
from config import appid, secret


user_api = Blueprint('user_api', __name__)


@user_api.route('/login', methods=['GET'])
def userLogin():
    code = request.values.get("code")  # 前端POST过来的微信临时登录凭证code
    if not code:
        return jsonify({'errmsg': 'Missing parameters: code', 'errcode': -2})
    print(code)
    # req_params: 用于发起code2Session请求的appID,appSecret等参数,调用此接口完成登录流程
    # todo: 这里需要替换成注册好的的微信小程序的appID和appSecret
    req_params = {
        'appid': appid,
        'secret': secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    # wx_login_api: code2Session请求api
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    # 向API发起GET请求
    response = requests.get(url=wx_login_api, params=req_params)
    # data: api获得的结果
    data = response.json()
    # 检查返回结果
    if 'errcode' in data:
        return jsonify(data)
    _openid = data['openid']  # 得到用户关于当前小程序的OpenID
    _session_key = data['session_key']  # 得到用户关于当前小程序的会话密钥session_key
    # 获取openid、session_key失败
    if not _openid or not _session_key:
        errmsg = data.get('errmsg', 'get session_key and openid fail')
        return jsonify({'errmsg': errmsg, 'errcode': -3})
    # 根据openid和session_key等信息进行身份验证，验证成功注册并录入数据库
    _token = generate_token(_openid, _session_key)
    res = user_verify(_openid, _token)
    # 1.openid,session_key,token都在数据库中,返回token和openid
    # 2.openid在数据库中,session_key更新了,生成新的token更新到数据库,返回token和openid
    # 3.openid,session_key,token都不在数据库中,相当于注册用户,将数据插入数据库
    # 4.数据库查询失败
    sql = ''''''
    args = ()
    if res == 4:
        return jsonify({'errmsg': 'Database query failed', 'errcode': -1})
    if res == 3:
        nkname = "用户".join(random.sample(string.ascii_letters + string.digits, 8))
        sql = '''
        insert into t_user(token,openid,session_key,nkname) 
        values (%s,%s,%s,%s);
        '''
        args = (_token, _openid, _session_key, nkname)
    elif res == 2:
        sql = "update t_user set token = %s, session_key=%s where openid = %s;"
        args = (_token, _session_key, _openid)
    result = updateToDB(sql, args)
    if 'errmsg' in result:
        return jsonify(result)
    # 返回自定义token等信息给前端，表示用户已经登录成功
    return jsonify({"msg": "login success", 'token': _token, 'openid': _openid})


@user_api.route('/avatar', methods=['POST'])
def postAvatar():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'missing parameters: token', 'errcode': -2})
    # 接收图片
    avatar = request.files.get('avatar')
    # 未获取头像文件
    if not avatar:
        return jsonify({'errmsg': 'missing parameters: avatar', 'errcode': -2})
    avatar_name = avatar.filename
    # 保存图片到  ./static
    filename = os.path.join(os.getcwd(), 'static/avatar', avatar_name)
    avatar.save(filename)
    # 删除旧头像
    sql = "select avatar from t_user where token = '{0}'".format(_token)
    results = getOneFromDB(sql)
    # 保存新头像文件名到数据库
    result = update_image_to_db(avatar_name, _token, "update t_user set avatar = %s where token = %s")
    if 'errmsg' in result:
        return jsonify(result)
    if results and 'errmsg' not in results:
        if results['avatar'] != 'default.jpg':
            delete_filename = os.path.join(os.getcwd(), 'static/avatar', results['avatar'])
            delete_image(delete_filename)
    return jsonify(result)


@user_api.route('/info', methods=['GET'])  # token => all info
def getUserInfo():
    _token = request.values.get("token")  # 前端POST过来的自定义用户态和
    # 缺少token参数
    if not _token:
        return jsonify({'errmsg': 'Missing parameters: token', 'errcode': -2})
    sql = "select * from t_user where token = %s"
    results = getOneFromDB(sql, _token)
    if not results or 'errmsg' in results:  # 数据库查询失败
        return jsonify(results)
    # 成功查询到用户信息
    results['avatar'] = sendAvatar(results['avatar'])  # 头像文件路径
    return jsonify(results)


@user_api.route('/search/<keyword>', methods=['GET'])
def getUserInfoBySearch(keyword):
    sql = "select * from user_preview where nkname like '%{0}%'".format(keyword)
    results = getAllFromDB(sql)
    if results and 'errmsg' not in results:
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
    return jsonify(results)


@user_api.route('/info/change', methods=['PUT'])
def changeUserInfo():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'Missing parameters: token', 'errcode': -2})
    data = dict(request.values)
    data.pop('token')  # 去除token字段
    if data:
        args = ""           # update 操作时 set后跟随的字符串
        params = []         # 需要更换的值values
        print('用户{0} 进行个人信息修改：'.format(_token))
        for key, value in data.items():
            print("{0}={1},".format(key, value))
            params.append(value)
            args = args + "{0}=%s,".format(key)
        args = args.rstrip(',')     # 去除最后一个 ','
        sql = "update t_user set " + args + " where token = '{0}'".format(_token)
        result = updateToDB(sql, params)
        if 'errmsg' in result:
            return jsonify(result)
    return jsonify({'msg': 'update data success'})


@user_api.route('/myroutes', methods=['GET'])
def getMyRoutes():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'Missing parameters: token', 'errcode': -2})
    _order = request.values.get("order")
    _ispub = request.values.get("ispublic")
    # 路线评分计算公式
    rubric = "((likenum*0.4)+(fork*0.3)+(round((lscore+rscore+tscore)/3, 1)*0.2)+(scoren*0.1)) pingfen"
    sql = '''select
    route_id,cover,avatar,title,descp,daynum,locnum,likenum,fork,round((lscore+rscore+tscore)/3, 1) as score,{0}
    from t_route r left join t_user u using(token)
    where r.token = '{1}';'''.format(rubric, _token)
    if _ispub:
        sql = sql.rstrip(';')
        sql += " and ispub = {0};".format(_ispub)
    if _order:
        sql = sql.rstrip(';')
        sql += " order by {0} desc;".format(_order)
    results = getAllFromDB(sql)
    if results or 'errmsg' not in results:
        for r in results:
            r['avatar'] = sendAvatar(r['avatar'])
            r['cover'] = sendCover(r['cover'])
    return jsonify(results)


@user_api.route('/mylikes', methods=['GET'])
def getMyLikes():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'missing token', 'errcode': -1})
    # 路线评分计算公式
    rubric = "((likenum*0.4)+(fork*0.3)+(round((lscore+rscore+tscore)/3, 1)*0.2)+(scoren*0.1)) pingfen"
    sql = '''select
    route_id,title,descp,daynum,locnum,likenum,fork,round((lscore+rscore+tscore)/3, 1) as score,{0}
    from t_route t right join lke l using(route_id) where l.token = %s;'''.format(rubric)
    results = getAllFromDB(sql, [_token])
    return jsonify(results)


@user_api.route('/myposts', methods=['GET'])
def getMyPosts():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'missing parameters: token', 'errcode': -2})
    sql = '''select post_id,p.title,CAST(endtime AS CHAR) endtime,p.descp,need,num,cover 
    from t_post p left join t_route r using(route_id) where p.token = '{0}' order by p.uptime desc;'''.format(_token)
    results = getAllFromDB(sql)
    if not results or 'errmsg' in results:
        return jsonify(results)
    for r in results:
        r['cover'] = sendCover(r['cover'])
    return jsonify(results)


@user_api.route('/myjoins', methods=['GET'])
def getMyJoins():
    _token = request.values.get("token")
    if not _token:
        return jsonify({'errmsg': 'missing parameters: token', 'errcode': -2})
    sql = '''select post_id,p.title,CAST(endtime AS CHAR) endtime,p.descp,need,num,cover 
    from members m left join t_post p using(post_id) left join t_route r using(route_id) 
    where m.token = '{0}' order by p.uptime desc;'''.format(_token)
    print(sql)
    results = getAllFromDB(sql)
    if not results or 'errmsg' in results:
        return jsonify(results)
    for r in results:
        r['cover'] = sendCover(r['cover'])
    return jsonify(results)
