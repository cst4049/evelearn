from bson import ObjectId
from flask import current_app as app


class XG_Class:
    @staticmethod
    def coll():
        col = app.data.driver.db['classes']
        return col
