import json

from bson import ObjectId
from flask import request, jsonify

from ms.models.BOK import BOKNode
from ms.models.BOT import BOTNode
from ms.models.BurTree import flattern_convertTo_tree
from ms.resources.unit import my_dump, objectIds_convert_json


def burrtree_son(id,suffix,burtree_node_type):
    """
    返回 botn 的子节点. 根据后缀返回 sonern or sonward
    :param id:
    :param suffix:
    :return:
    """
    if burtree_node_type == "bok":
        db_collection = BOKNode.coll()
    else:
        db_collection = BOTNode.coll()
    list = []
    if suffix == 'sonward':
        recursion_structuring(id, list, db_collection )

    if suffix == 'sonern':
        recursion_structuring(id, list, db_collection )
        #因为 最后加入的是 本节点.所以直接pop最后一个就可以了.
        #如果后续加入 排序 此方法不可用
        if list == []:
            return jsonify({"_items":"找不到该节点"}),404
        list.pop()

    flag_structure = request.args.get("structure")
    if flag_structure == 'tree':
        tree = flattern_convertTo_tree(list)
        #如果查询条件 并且是有comboformat的说明是 英语题型
        if request.args.get("where") != None:
            #走剪枝的路线
            query_condition = json.loads(request.args.get("where"))
            comboformat = query_condition.get("comboformat")
            if comboformat != None:
                # 走英语缓存
                # 默认返回 tree.
                vocabulary_name = "vocabulary3000"
                phrase_name = "phrase2000"
                english_dict = {
                    "fillWordInText": ["词法", "句法", "翻译短语"],
                    "simpleSelection": ["词法", "句法", "单项选择"],
                    "fillWordInSentence": ["词法", "句法", "单句填空"],
                    "phraseTranslation": ["词法", "句法", vocabulary_name, phrase_name, "翻译短语"],
                    "sentenceTranslation": ["词法", "句法", vocabulary_name, phrase_name, "翻译句子"],
                    "patternTransformation": ["词法", "句法", "句型转换"],
                    "sentenceCompletion": ["词法", "句法", vocabulary_name, phrase_name, "完成句子"]
                }
                result_list = []
                if comboformat in english_dict.keys():

                    for temp in tree:
                        if temp['name'] in english_dict[comboformat]:
                            result_list.append(temp)

                else:
                    for temp in tree:
                        if temp['name'] == comboformat:
                            result_list.append(temp)

                return objectIds_convert_json({"_items": result_list})

        return jsonify({'_items': json.loads(my_dump(tree))})
    return jsonify({'_items': json.loads(my_dump(list))})




def recursion_structuring(_id ,list,mongoDB_collection):
    """
    用递归的方式 把ID对应的botn节点本身和他所有的后代都返回到一个list里
    :param _id:
    :param list:
    :param mongoDB_collection:
    :return:
    """
    node = mongoDB_collection.find_one({'_id':ObjectId(_id)})
    if node != None:
        if 'son' in node.keys():

            for son_item in node['son']:
                if type(son_item) != type({}):
                    recursion_structuring(son_item, list, mongoDB_collection)
        list.append(node)
    pass