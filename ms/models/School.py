from bson import ObjectId
from flask import current_app as app


class School:
    @staticmethod
    def coll():
        col = app.data.driver.db['schools']
        return col
