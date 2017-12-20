from bson import ObjectId
from flask import current_app as app


class Student:
    @staticmethod
    def coll():
        col = app.data.driver.db['students']
        return col
