from bson import ObjectId
from flask import current_app as app


class SeminarSpans:
    @staticmethod
    def coll():
        col = app.data.driver.db['seminar_spans']
        return col

