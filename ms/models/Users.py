from bson import ObjectId
from flask import current_app as app


class Users:
    @staticmethod
    def coll():
        col = app.data.driver.db['users']
        return col

    @staticmethod
    def find_one_obj(user_id):
        return Users.coll().find_one({"_id":ObjectId(user_id), "_deleted":False})

    @staticmethod
    def update_one(id ,passwd):
        result = Users.coll().update({"_id":ObjectId(id)},{"$set":{"passwd":passwd}})
        if result:
            return "success"
        return "error"