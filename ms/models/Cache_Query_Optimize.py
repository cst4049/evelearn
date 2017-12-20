from flask import current_app as app


class Cache_Query_Optimize():


    @staticmethod
    def coll():
        col = app.data.driver.db['cache_query_optimize']
        return col

