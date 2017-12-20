import json

from bson import ObjectId

from ms.models.BOT import BOTNode
from ms.models.BOTT import BOTT
from ms.models.BurTree import flatten_burtree_by_recursion


def post_POST_bott(resource, request, lookup):
    if resource=='bott' and lookup._status_code == 201:
        resp = json.loads(lookup.data.decode('utf-8'))
        _id = resp["_id"]
        bottCollection = BOTT.coll()
        botTree = bottCollection.find_one({'_id':ObjectId(_id)})
        #获取root 节点
        rootNode = botTree.pop('root')
        rootNode.update(dad=ObjectId(_id))
        # 将教材的版本传入
        rootNode.update(edition=botTree['edition'])
        #root树 扁平化
        list = []
        flatten_burtree_by_recursion(rootNode,list)
        #插入botn中
        botnCollection = BOTNode.coll()
        print("list",list)
        botnCollection.insert(list)
        #root节点保存 root对应的objectId
        bottCollection.update({'_id': ObjectId(_id)}, {'$set':{"root": list[-1]['_id']}})
        pass
