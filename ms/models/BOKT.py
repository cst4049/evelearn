from flask import current_app as app


class BOKT():


    @staticmethod
    def coll():
        return  app.data.driver.db['bokts']

