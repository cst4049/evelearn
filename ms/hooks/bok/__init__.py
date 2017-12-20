import json

from bson import ObjectId

from ms.models.BOK import BOKNode
from ms.models.BOKT import BOKT
from ms.models.BurTree import flatten_burtree_by_recursion


def post_POST_bokt(resource, request, lookup):
    """
    0.已经把树存到db中
    1.找到该节点,获取root的值
    2.将版本号传入root节点里
    3.*调用 扁平化方法.返回一个list*
    4.将list存入bokn中
    5.把树替换成对应的id
    """
    if resource == "bokt" and lookup._status_code == 201:
        resp = json.loads(lookup.data.decode('utf-8'))
        _id = resp["_id"]
        boktCollection = BOKT.coll()
        bokTree = boktCollection.find_one({'_id':ObjectId(_id)})
        #获取root 节点
        rootNode = bokTree.pop('root')
        rootNode.update(dad=ObjectId(_id))
        # 将教材的版本传入
        rootNode.update(edition=bokTree['edition'])


        #root树 扁平化
        list = []
        flatten_burtree_by_recursion(rootNode,list)
        #插入botn中
        boknCollection = BOKNode.coll()
        boknCollection.insert(list)
        #root节点保存 root对应的objectId
        boktCollection.update({'_id': ObjectId(_id)}, {'$set':{"root": list[-1]['_id']}})
        pass




def post_POST_bokn_son(request, lookup):
    _data =  json.loads(lookup.data.decode("utf-8"))
    _id = _data.get("_id")
    if _id != None:
        ins = BOKNode.coll().find_one({
            "_id": ObjectId(_id),"_deleted":False
        })
        if ins != None:
            dad_id = ins['dad']
            dad_ins = BOKNode.coll().find_one({
                "_id":dad_id
            })

            dad_son_list = dad_ins.get("son")
            if dad_son_list != None:
                dad_son_list.append(ins["_id"])
            else:
                dad_son_list =[ins["_id"]]

            BOKNode.coll().update({"_id":dad_id},{"$set":{"son":dad_son_list}})


    pass