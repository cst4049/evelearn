from bson import ObjectId,Decimal128
from decimal import Decimal
from flask import g,abort
from sc.question_fingerprint import doall
from sc.question_similarity.similar_check import similar_check

from ms.hooks.taginfo import ques_split, \
    add_subsource, add_subsourceloca, \
    add_subresponseFormat, add_subcomboFormat,\
    add_derivedPath
from ms.models.Question import Question


def before_returning_questions(response):
    for ques in response["_items"]:
        ques["subkoSource"] = add_subsource(ques)
        ques["subsourceLoca"] = add_subsourceloca(ques)
        ques["subresponseFormat"] = add_subresponseFormat(ques)
        ques["subcomboFormat"] = add_subcomboFormat(ques)


def before_returning_question(response):
    response["subkoSource"] = add_subsource(response)
    response["subsourceLoca"] = add_subsourceloca(response)
    response["subresponseFormat"] = add_subresponseFormat(response)
    response["subcomboFormat"] = add_subcomboFormat(response)
    response["path"] = add_derivedPath(response)


def before_insert_question(items):
    itemson = []
    for item in items:
        content = item.get("contOfQuery")
        hashcode = doall(content)
        simhash_1, simhash_2, simhash_3, simhash_4 = hashcode >> 48, (hashcode >> 32) & 0x0000ffff, (
        hashcode >> 16) & 0x00000000ffff, hashcode & 0x000000000000ffff
        update = {
            "simhash": Decimal128(Decimal(hashcode)),
            "simhash_1": simhash_1,
            "simhash_2": simhash_2,
            "simhash_3": simhash_3,
            "simhash_4": simhash_4
        }
        if not similar_check((simhash_1, simhash_2, simhash_3, simhash_4))[0]:
            item.update(update)
        else:
            abort(409, description="相似文档已存在")

        item["typewritedByFirstly"] = g.user.get("_id")
        sonCount = item.get("sonCount")
        if sonCount and sonCount > 1 :
            ques_split(itemson,item)
        item["state"] = Question.on_signal(item.get("_id"), 'created')
    items.extend(itemson)


def after_inserted_questions(items):
    pass


def before_update_question(update,original):
    """
    含有子题的patch操作
    :param update:
    :param origin:
    :return:
    """
    # todo patch sonquestions
    if update.get("sonCount") == 0 and original.get("sonCount") > 1:
        Question.coll().remove({"_id": {"$in": original.get("son")}})
        Question.coll().update({"_id": original.get("_id")}, {"$unset": {"son": 1}})
    if update.get("sonCount") > 1:
        if original.get("sonCount") >1 :
            Question.coll().remove({"_id": {"$in": original.get("son")}})
            Question.coll().update({"_id": original.get("_id")}, {"$unset": {"son": 1},"$set":{"contOfKey":""}})
        else:
            Question.coll().update({"_id": original.get("_id")}, {"$set": {"contOfKey": ""}})
        origin_id = ObjectId() if not original.get("_id") else original.get("_id")
        son_question = update.pop('fieldOfSon')
        soncount = update.pop('sonCount')

        fieldK = [k for k, v in son_question.items() if v]
        fieldV = [v for k, v in son_question.items() if v]  # 解答题有子题，但是没有子属性
        if fieldV:
            if son_question.get("contOfKey"):  # 如果子属性有答案使用子属性的答案
                update.pop("contOfKey")
            son_extra = [dict(map(lambda x, y: [x, y[i]], fieldK, fieldV),
                              _id=ObjectId(), dad=origin_id, **update) for i in range(len(fieldV[0]))]
        else:
            son_extra = [dict({'_id': ObjectId(), 'dad': origin_id}, **update) for i in range(soncount)]
        son = [son['_id'] for son in son_extra]
        Question.coll().insert(son_extra)
        update.update(son=son, sonCount=soncount,
                      fieldOfSon=son_question,
                      _id=origin_id)


def before_update_question2(update,original):
    """
    含有子题的patch操作
    :param update:
    :param origin:
    :return:
    """
    # todo patch sonquestions
    original_soncount = original.get("sonCount")
    update_soncount = update.get("sonCount")
    original.update(update)
    original_id = original.get("_id")
    lookup = {"_id": {"$ne": original_id}}
    content = update.get("contOfQuery")
    hashcode = doall(content)
    simhash_1, simhash_2, simhash_3, simhash_4 = hashcode >> 48, (hashcode >> 32) & 0x0000ffff, (
        hashcode >> 16) & 0x00000000ffff, hashcode & 0x000000000000ffff
    hashseg = {
        "simhash_1": simhash_1,
        "simhash_2": simhash_2,
        "simhash_3": simhash_3,
        "simhash_4": simhash_4
    }
    if not similar_check((simhash_1, simhash_2, simhash_3, simhash_4), lookup)[0]:
        update.update(hashseg)
    else:
        abort(409, description="相似文档已存在")

    original_state = original.pop("state",None)

    if original_soncount == 0 and update_soncount > 1:
        itemson = []
        ques_split(itemson,original)
        update.update(original)
        update.update(state=original_state)
        Question.coll().insert(itemson)

    elif original_soncount > 1:
        if update_soncount == 0:
            sid = update.get("fieldOfSon").pop("sid",None)
            son = original.get("son")
            update.update(_id=original_id,state=original_state)
            if sid:
                sidinfo = Question.coll().find_one({"_id": sid[0]})
                if sidinfo:
                    sidinfo.update(update)
                    update.update(sidinfo)
                    update.pop("dad")
            Question.coll().remove({"_id": {"$in": son}})
            Question.coll().update({"_id": original_id}, {"$unset": {"son": 1}})

        elif update_soncount > 1:
            original.pop("_id")
            son_old = original.pop("son")
            son_question = original.pop('fieldOfSon')
            soncount = original.pop('sonCount')
            # typewritedByFirstly = original.pop('typewritedByFirstly')#子题不保存录入人
            # typewritedAtFirstly = original.pop('typewritedAtFirstly')

            fieldK = [k for k, v in son_question.items() if v]
            fieldV = [v for k, v in son_question.items() if v]
            if fieldV:
                if son_question.get("contOfKey"):  # 如果子属性有答案使用子属性的答案
                    original.pop("contOfKey")
                son_extra = [dict(map(lambda x, y: [x, y[i]], fieldK, fieldV),
                             dad=original_id, **original) for i in range(len(fieldV[0]))]
            else:
                son_extra = [dict({'dad': original_id}, **original) for i in range(soncount)]
            for quest in son_extra:
                sid = quest.pop("sid",None)
                state = quest.pop("state", None)
                quest["_id"] = sid or ObjectId()
                if sid:
                    sidinfo = Question.coll().find_one({"_id": sid})
                    if sidinfo:
                        sidinfo.update(quest)

            son = [quest.get("_id") for quest in son_extra]
            Question.coll().remove({"_id": {"$in": son_old}})
            [Question.coll().update({"_id":ques.get("_id")},ques,True) for ques in son_extra if ques]
            update.update(son=son, sonCount=soncount,
                          fieldOfSon=son_question,
                          _id=original_id,
                          state=original_state)