from flask import current_app as app


class Enum:


    @staticmethod
    def coll():
        col = app.data.driver.db['enums']
        return col
