
import json
import os

from ms.models.BOK import BOKNode
from ms.models.BOKT import BOKT
from ms.models.BOT import BOTNode
from ms.models.BOTT import BOTT
from ms.models.BurTree import flatten_burtree_by_recursion
from ms.models.ENUM import Enum
from ms.models.PROPERTYSET import PropertySet
from ms.models.ROLE import Role
from ms.resources.bok import strucutre_word_list

"""
思路: 
通过预置user 拿token. 
拿到token
然后在每个请求里面带token
"""

def init_meta():
    f = open("./meta-data/src/bok/bok.json")
    f_obj = json.loads(f.read())
    burtree_converto_list_insertDB(f_obj)
    f.close()

    f = open ("./meta-data/src/bot/bot.json")
    f_obj = json.loads(f.read())
    burtree_converto_list_insertDB(f_obj)
    f.close()



    file_path = "./meta-data/src/vocabulary_phrase/"
    lists = []
    file_list = os.listdir(file_path)
    for file_item in file_list:
        file_item_obj = json.loads(open(file_path + file_item).read())
        strucutre_word_list(file_item_obj)

    file_path = "./meta-data/src/enum/"
    lists = []
    file_list = os.listdir(file_path)
    for file_item in file_list:
        file_item_obj = json.loads(open(file_path +file_item).read())
        lists.append(file_item_obj)
    Enum.coll().insert(lists)



    file_path = "./meta-data/src/propertySet/edit/"
    lists = []
    file_list = os.listdir(file_path)
    for file_item in file_list:
        file_item_obj = json.loads(open(file_path + file_item).read())
        lists.append(file_item_obj)
    PropertySet.coll().insert(lists)


    file_path = "./meta-data/src/propertySet/mark/"
    lists = []
    file_list = os.listdir(file_path)
    for file_item in file_list:
        file_item_obj = json.loads(open(file_path + file_item).read())
        lists.append(file_item_obj)
    PropertySet.coll().insert(lists)


    file_path = "./meta-data/src/role/"
    lists = []
    file_list = os.listdir(file_path)
    for file_item in file_list:
        file_item_obj = json.loads(open(file_path + file_item).read())

        # 因为role 是写在一起的。所以不需要要添加到lists中
        Role.coll().insert(file_item_obj)



def burtree_converto_list_insertDB (burtreeNode):
    root_node = burtreeNode.pop("root")
    # 将其转成list
    if "bok" in burtreeNode['name']:
        db_collection = BOKNode.coll()
        tree_collection = BOKT.coll()
    else:
        db_collection = BOTNode.coll()
        tree_collection = BOTT.coll()
    dad_id = tree_collection.insert(burtreeNode)
    root_node.update(dad=dad_id)
    root_node.update(edition=burtreeNode['edition'])

    list = []
    flatten_burtree_by_recursion(root_node,list)
    db_collection.insert(list)
