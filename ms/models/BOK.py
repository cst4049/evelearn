from flask import current_app as app

from ms.models.BurTree import BurTreeNode;


class BOKNode(BurTreeNode):


    @staticmethod
    def coll():
        return  app.data.driver.db['bokns']


    @staticmethod
    def dadHomlyro(id):
        pass


    @staticmethod
    def all_bokn(id):
        return BOKNode.coll().find({"_id":id,"_deleted":False},{})

    @staticmethod
    def find_one_by_edition_name(name,edition):
        return BOKNode.coll().find_one({"name":name,"edition":edition})

    @staticmethod
    def find_by_edition_name(name,edition):
        return BOKNode.coll().find({"name":name,"edition":edition})
