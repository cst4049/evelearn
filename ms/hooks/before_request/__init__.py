import time

import jwt
from flask import current_app as app
from flask import request, abort, g

import init_util.init_meta_data
from ms.models.Users import Users


def delay():
    delay = app.config.get('DEBUG_DELAY')
    time.sleep(delay)


def record():
    token = request.args.get("token")
    if token:
        user = g.user.get("name")
    else:
        user = request.args.get("username")

    if request.method in ["POST","PATCH","DELETE"]:
        lookup = dict(
            record_time=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
            method=request.method,
            url=request.url,
            user = user
        )
        log = app.data.driver.db['log']
        log.insert(lookup)


def interpretor():
    token = request.args.get("token")
    if token :
        try:
            payload = jwt.decode(token, 'zyc', algorithm='HS256')
            lookup = dict(name=payload.get("username"),
                          role=payload.get("role")
                          )
            uinfo = Users.coll().find_one(lookup)
            if uinfo:
                g.user = uinfo #将用户信息存入临时全局变量中
            else:
                abort(401, description="please check your token")
        except Exception as e:
            abort(401,description="please check your token")
    elif request.method == "POST" and \
            request.args.get("username") and \
            request.args.get("passwd"):
        pass
    #  琛 新增 接口heartbeat 不需要token验证
    elif request.method == "HEAD" and request.path in "/heartbeat":
        pass
    elif request.method == "GET" and "media" in request.path:
        pass
    #
    elif request.method == "POST" and \
            request.path in "/init/":
        data = list(Users.coll().find())
        if data:
            abort(403,description="the system already init")
        else:
            init_util.init_meta_data.init_meta()
    else:
        abort(401,description="token not set")

def signal():
    method = request.method
    path = request.path
    if method == "POST" and path == "/quesbanks/core/questions" or \
        path == "/quesbanks/core/questions":
        request.json.update(state=1)
    elif method == "SPUR":
        pass
    print('aa')