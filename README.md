# 旅小库微信小程序后端接口

## 介绍
该项目为旅小库微信小程序后端接口，基于Flask框架，使用Python语言进行开发。服务器框架为uwsgi+nginx框架。
> Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 ，较其他同类型框架更为灵活、轻便、安全且容易上手，适用于快速开发小型 Web 应用、接口API等等。

内部与数据库连接使用的是pymysql包，pymysql连接数据库方便、快捷，并且接收事务返回结果、报错信息等方法简单。
## 目录结构
```
.
|-- README.md
|-- note
|   `-- nginx+uswgi.txt
|-- static
|   |-- avatar              # 头像图片
|   |-- cover               # 封面图片
|   `-- test.txt
|-- swagger
|   |-- api.yml             # 接口文档
|   `-- test.yml
|-- uwsgi
|    `-- lxkapi.ini         # uwsgi配置文件
|-- app.py                  # 主程序文件
|-- data.json
|-- dbconnect.py
|-- download.py
|-- list.txt
|-- post.py
|-- requirements.txt
|-- routeEdit.py
|-- routes.py
|-- score.py
|-- test.json
|-- test.md
|-- test.py
|-- test.txt
|-- tools.py
|-- tree.txt
`-- user.py
```
### 主要文件介绍
- app.py: 主程序文件，启动项目时，运行此文件。
- dbconnect.py: 数据库连接文件，包含一个数据库连接类，用于连接数据库，接收请求参数，返回结果，其中db_info为数据库连接信息，部署到本地时需要修改。
- tools.py: 工具文件，用于处理一些常用功能，如生成token、图片处理、连接数据库等。
- user.py: 和用户相关的接口，用于登录、修改、查看个人信息等。
- routes.py: 和路线查看相关的接口。
- routeEdit.py: 路线编辑接口，用于编辑路线。
- post.py: 和帖子操作相关的接口，用于发布、删除、修改、查看帖子。
- score.py: 和评分相关的接口，用于发布、删除、修改、查看评分。
- download.py: 下载文件接口，主要用于头像、路线图片。
- uwsgi/lvkapi.ini: uwsgi配置文件，用于配置uwsgi运行环境。
- swagger/api.yml: 接口文档文件，和swagger搭配生成接口文档。
- route.json: 路线信息的数据结构示例。
- static：静态文件目录，用于存放头像图片、路线封面图片等。
- notes/nginx+uswgi.txt: nginx+uwsgi部署说明。


## 使用说明
### 环境准备
项目依赖的环境、类库有：[requirements.txt](requirements.txt)
启动项目前,在终端输入`pip install -r requirements.txt`安装依赖环境。

### 启动项目
启动项目时，需要修改config.py文件中的信息。
需要更改的地方有：
1. 数据库连接信息
2. 小程序appid和secret

```
# 数据库连接信息
db_info = {
    host = 'localhost'
    user = 'root'             # 数据库用户名
    password = 'password'     # 数据库密码
    database = 'dbname'       # 数据库名称
}

# 小程序appid和secret
appid = 'your_appid'
secret = 'your_secret'
```

在本地运行时，在终端输入`python app.py`启动项目或者直接运行app.py文件。
运行之后，终端显示
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://your_ip_address:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 826-632-973
```
这时，项目已经启动成功，可以通过浏览器访问`http://localhost:5000`或者`http://your_ip_address:5000`使用相关接口,在`http://localhost:5000/apidocs` 可以查看接口文档。


### api接口文档
<https://api.lvxiaoku.com.cn/apidocs>


