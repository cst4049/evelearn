from bson import ObjectId
from flask import request, jsonify

from ms.models.Users import Users


def change_passwd(user_id):
    '''
    修改Users的密码,只能通过patch提交
    :param user_id:
    :return:
    '''

    passwd = request.json.get("passwd")

    user_ins =  Users.find_one_obj(user_id)

    if user_ins == None :

        return jsonify({"errorMsg": "账号不存在."})
    else :
        Users.coll().update({"_id":ObjectId(user_id)},{"$set":{"passwd":passwd}})
        return jsonify({"msg":"修改成功"})

