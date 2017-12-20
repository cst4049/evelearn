from bson import ObjectId
from flask import current_app as app


class Seminar:
    @staticmethod
    def coll():
        col = app.data.driver.db['seminars']
        return col

