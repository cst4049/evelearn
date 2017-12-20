from bson import ObjectId
from flask import current_app as app


class Teacher:
    @staticmethod
    def coll():
        col = app.data.driver.db['teachers']
        return col
