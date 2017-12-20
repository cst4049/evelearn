from flask import current_app as app

from ms.models.BurTree import BurTreeNode;


class BOTNode(BurTreeNode):


    @staticmethod
    def coll():
        return app.data.driver.db['botns']


    @staticmethod
    def dadHomlyro(id):
        pass


    @staticmethod
    def all_botn(id):
        BOTNode.coll().find({"_id":id,"_deleted":False},{})
