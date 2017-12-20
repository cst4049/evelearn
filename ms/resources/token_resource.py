import base64
import json

import arrow
import jwt
from flask import request, jsonify

from ms.models.Users import Users
from ms.resources.unit import my_dump


def check_token():
    """
    生成token
    :return:
    """
    header = {"typ": "JWT", "alg": "HS256"}
    token = request.args.get('token')
    if token :
        try:
            payload = jwt.decode(token, 'zyc', algorithm='HS256')
        except Exception as e:
            return jsonify({"reson": "token 不正确"})
        payload.update(exp=str(arrow.get().timestamp))
        Token = {}
        Token.update(header=base64.encodebytes(json.dumps(header).encode()))
        Token.update(payload=base64.encodebytes(json.dumps(payload).encode()))
        encoded = jwt.encode(payload, 'zyc', algorithm='HS256')
        Token.update(encoded=encoded)
        return jsonify(Token)

    else:
        args = request.args
        username = args['username']
        passwd = args['passwd']

        userCollection = Users.coll()

        result_user = userCollection.find_one({'name':username,'_deleted':False})


        if result_user == None:
            return jsonify({"errorMsg":"用户不存在或者密码错误"})

        if result_user['passwd'] == passwd:

            #加密逻辑
            exp_time = str(arrow.get().timestamp
                           + 8 * 60 * 60
                           )
            payload = {
                      "exp": exp_time,
                      "timestamp": str(arrow.get().timestamp),
                      "description":result_user["description"],
                      "discipline":result_user["discipline"],
                      "role":result_user['role'],
                      "username": result_user['name'],
                      "primaryRole":result_user['primaryRole'],
                      "uid":str(result_user["_id"])
                       }
            if result_user.get("school")!=None:
                payload.update(school=my_dump(result_user['school']))
            payload_64 = base64.encodebytes(json.dumps(header).encode())#base64
            header_64 =  base64.encodebytes(json.dumps(payload).encode())
            encoded = jwt.encode(payload, 'zyc', algorithm='HS256')
            print("encoded",encoded)
            result_token = {"header": header_64, "payload": payload_64, "encoded":encoded}
            print(jwt.decode(encoded, 'zyc', algorithm='HS256'))
            return jsonify(result_token)

        else:
            
            return jsonify({"errorMsg":"账户或密码不正确"})






def checktoken():
    """
    验证密码
    :return:
    """


    pass