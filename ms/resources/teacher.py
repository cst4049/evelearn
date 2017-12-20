
import json
import re

import arrow
from bson import ObjectId

from ms.models.Grade import Grade
from ms.models.XG_Class import XG_Class
from ms.resources.unit import my_dump


def post_GET_teachers_append_classTeached(request, payload):
    _data = json.loads(payload.response[0].decode('utf-8'))
    #####如果是 精确查找. /resource/id 这种类型的,是否返回数据? 目前不返回.
    if _data.get("_items") != None:
        school_id = re.search('[a-f0-9A-F]{24}', request.base_url).group()
        teacher_list = _data.get("_items")
        cls_list = list(XG_Class.coll().find({"school": ObjectId(school_id),"_deleted":False}))
        teacher_list_new = []
        for temp_teacher in teacher_list:
            cls_teached_list = []
            for temp_cls in cls_list:
                for t_role in temp_cls.get("teacherTrole"):
                    if t_role.get("teacher") == ObjectId(temp_teacher.get("_id")):
                        #这里增加title
                        _grade_id = temp_cls.get("grade")
                        #如果是学科班 使用code
                        if _grade_id == None:
                            title = temp_cls.get("code")
                        else:
                        #如果是传统班和行政班 使用年级 + code
                            grade_ins =Grade.coll().find_one({
                                "_id": temp_cls.get("grade")
                            })
                            title = str(arrow.get(grade_ins.get("birth")).year) + "级 " + temp_cls.get("code")
                        temp_cls.update(title=title)
                        cls_teached_list.append(temp_cls)
                        break

            temp_teacher.update(classTeached=cls_teached_list)
            teacher_list_new.append(temp_teacher)

        _data["_items"] = teacher_list_new
        payload.response[0] = my_dump(_data)
        payload.content_length = len(my_dump(_data))
    pass