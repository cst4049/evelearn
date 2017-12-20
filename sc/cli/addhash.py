from sc.question_fingerprint import *
from sc.question_similarity.similar_check import similar_check
import bson
from bson.decimal128 import Decimal128
from decimal import Decimal
from bson import ObjectId

def addcode(collection,scope):
    """数据库批量增加hashcode字段"""
    # if isinstance(quest,dict):
    #     quest = [quest]
    # for q in quest:
    #     content = q.get("contOfQuery")
    #     beaut_cont = beauty_cont(content)
    #     after_jieba = participle(beaut_cont)
    #     real_word = remove_stop_word(after_jieba)
    #     hashcode = simhash(real_word)[2:]
    #     hashseg_1,hashseg_2,hashseg_3,hashseg_4 = hashcode[:16],hashcode[16:32],hashcode[32:48],hashcode[48]
    col = db[collection]
    projection = {
        "_id":1,
        "contOfQuery":1
    }
    scope.update(
        {"dad":{"$exists":False},
         "_deleted": False
         }
    )
    datas = col.find(scope,projection)
    for data in datas:
        content = data.get("contOfQuery")
        hashcode = doall(content)
        simhash_1,simhash_2,simhash_3,simhash_4 = hashcode >> 48,(hashcode >> 32) & 0x0000ffff ,(hashcode >> 16) & 0x00000000ffff,hashcode & 0x000000000000ffff
        lookup = {"_id":data.get("_id")}
        update = {
            "simhash": bson.Decimal128(Decimal(hashcode)),
            "simhash_1":simhash_1,
            "simhash_2":simhash_2,
            "simhash_3":simhash_3,
            "simhash_4":simhash_4
        }
        col.update_one(lookup,{"$set":update})
#
#
# def newquest(question,lookup=None):
#     if not lookup:
#         lookup = {}
#     content = question.get("contOfQuery")
#     hashcode = doall(content)
#     hashseg_1, hashseg_2, hashseg_3, hashseg_4 = hashcode >> 48,(hashcode >> 32) & 0x0000ffff ,(hashcode >> 16) & 0x00000000ffff,hashcode & 0x000000000000ffff
#     update = {
#         "hashseg1": hashseg_1,
#         "hashseg2": hashseg_2,
#         "hashseg3": hashseg_3,
#         "hashseg4": hashseg_4
#     }
#     if not similar_check((hashseg_1,hashseg_2,hashseg_3,hashseg_4),lookup)[0]:
#         question.update(update)
#         return question
#     abort(409,description="相似文档已存在")