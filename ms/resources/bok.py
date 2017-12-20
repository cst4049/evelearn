import json

from bson import ObjectId
from flask import request, jsonify

from ms.models.BOK import BOKNode


# def english_bokn_query(bok_type):
#     """英语知识点查询接口
#
#         获取查询条件.
#         通过查询条件去找节点.
#         调用递归遍历该节点的所有子节点
#     """
#     condition = request.args["where"]
#     structure = request.args['structure']
#     condition =json.loads(condition)
#
#     #查询节点 ,然后调用递归的方法.
#     bok_obj = BOKNode.find_by_edition_name(bok_type,condition["edition"])
#
#     if bok_obj == None:
#         return jsonify(_items="暂未找到资源"),404
#
#
#     result = []
#     tree_list = []
#     bokn_name =""
#     for temp in bok_obj:
#         result.append(temp)
#         bokn_name = temp["name"]
#     #返回 词法 句法
#     if bokn_name in ["fillWordInText",
#                      "simpleSelection",
#                      "fillWordInSentence",
#                      "phraseTranslation",
#                      "sentenceTranslation",
#                      "patternTransformation",
#                      "sentenceCompletion"]:
#         morphology = BOKNode.find_one_by_edition_name("词法",condition["edition"])
#         syntax = BOKNode.find_one_by_edition_name("句法",condition["edition"])
#         temp_list = []
#         recursion_structuring(morphology["_id"],temp_list,BOKNode.coll())
#         morphology_list = temp_list
#         temp_list = []
#         recursion_structuring(syntax["_id"],temp_list,BOKNode.coll())
#         syntax_list = temp_list
#         tree_list.append(morphology_list)
#         tree_list.append(syntax_list)
#         pass
#
#     #返回词汇和固定搭配
#     if bokn_name in ["phraseTranslation","sentenceTranslation","patternTransformation","sentenceCompletion"]:
#         vocabulary_list = Vocabulary_phrase.find_one_by_name("vocabulary3000")
#         phrase_list = Vocabulary_phrase.find_one_by_name("phrase2000")
#         result.append(vocabulary_list)
#         result.append(phrase_list)
#         pass
#
#
#     # 将列表转成树
#     if structure == "tree":
#         for tree_item in tree_list:
#             result.append(flattern_convertTo_tree(tree_item))
#
#     return objectIds_convert_json({"_items":result})



def english_word_list_insert():
    temp = request.data
    post_args = json.loads(str(temp, encoding='utf-8'))
    strucutre_word_list(post_args)
    return jsonify({"_item":"success"}),200


def strucutre_word_list(obj):
    post_args = obj
    bokn_list = post_args['word']
    if post_args.get('edition') == None:
        edition = 'std-17'
    else:
        edition = post_args['edition']

    english_node = BOKNode.coll().find_one({"name": "english", "edition": edition})
    english_id = english_node.get("_id")
    # 这里对 词汇或者短语的name 进行处理
    english_result = BOKNode.coll().find({"name": post_args.get("name"), "edition": edition})
    if english_result.count() > 0:
        return jsonify({"_items": "name is not unique"}), 422
    root_objId = ObjectId()
    root_dict = {
        "_id": root_objId,
        "name": post_args.get("name"),
        "title": post_args.get("name"),
        "description": post_args.get("description"),
        "koLyri": "just",
        "koLyro": "area",
        "dad": english_id,
        "edition": edition
    }
    english_son_list = english_node.get("son")
    if type(english_son_list) != type([]):
        english_son_list = [english_son_list]
    english_son_list.append(root_objId)

    BOKNode.coll().update({"_id": english_node.get("_id")}, {"$set": {"son": english_son_list}})
    son_list = []
    son_obj_list = []
    for bokn_temp in bokn_list:
        son_id = ObjectId()
        temp_dict = {
            "name": bokn_temp,
            "title": bokn_temp,
            "koLyri": "just",
            "koLyro": "point",
            "edition": edition,
            "_id": son_id,
            "dad":root_objId
        }
        son_list.append(son_id)
        son_obj_list.append(temp_dict)
    root_dict.update(son=son_list)
    son_obj_list.append(root_dict)
    BOKNode.coll().insert(son_obj_list)
    pass