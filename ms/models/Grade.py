from bson import ObjectId
from flask import current_app as app


class Grade:
    @staticmethod
    def coll():
        col = app.data.driver.db['grades']
        return col
