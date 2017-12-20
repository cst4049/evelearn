from flask import current_app as app


class BOTT():


    @staticmethod
    def coll():
        return app.data.driver.db['botts']

