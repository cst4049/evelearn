from flask import current_app as app


class PropertySet:


    @staticmethod
    def coll():
        col = app.data.driver.db['propertysets']
        return col
