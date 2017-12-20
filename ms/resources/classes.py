import json
import re

import arrow
from bson import ObjectId
from flask import request, jsonify
from  werkzeug.datastructures import ImmutableMultiDict

from ms.models.Grade import Grade
from ms.models.Student import Student
from ms.models.Teacher import Teacher
from ms.models.XG_Class import XG_Class
from ms.resources.grade import get_grades_by_time, set_title_by_grade
from ms.resources.unit import my_dump


# def query_class_list(school_id):
#     """
#     思路：
#     1. 查询班级
#         人数
#         classKind
#         directionKind
#         最后更改时间
#
#     2. 查询班级的年级信息
#         birth
#         _id
#
#     3. 查询班级的老师信息
#         name
#         _id
#
#     4. 将class 中的 teacher 替换成对应信息, grade 同理.
#
#     :return:
#     """
#     query_dict = json.loads(request.args.get("where"))
#
#
#     query_dict.update(school=ObjectId(school_id))
#
#
#     if query_dict.get("grade") == None:
#         query_dict.pop('grade')
#     else:
#         query_dict.update(grade=ObjectId(query_dict.get("grade")))
#
#     if query_dict.get("classKind") == None:
#         query_dict.pop("classKind")
#         pass
#     else:
#         query_dict.update(classKind=query_dict.get("classKind"))
#
#
#     query_dict.update(_deleted=False)
#     _result = XG_Class.coll().find(query_dict)
#
#     #查到满足条件的班级
#     list_temp = []
#     for item in _result:
#         list_temp.append(item)
#
#     #查找所有的 grade
#     _grade_list = list(set([item['grade'] for item in list_temp]))
#     query_dict.clear()
#
#
#     query_dict.update({"_id":{"$in":_grade_list},"_deleted":False})
#     grade_list =list( Grade.coll().find(query_dict))
#
#     #将class 里面的grade 换成对应的instance
#     for item in grade_list:
#         for index in range(len(list_temp)):
#             if item["_id"] == list_temp[index]["grade"] :
#                 list_temp[index]["grade"]=item
#                 pass
#
#
#     #查找所有的老师
#     _teacher_list = list(set([item.get('teacherSrole') for item in list_temp]))
#     query_dict.clear()
#     teacher_list = []
#     for item in _teacher_list:
#         teacher_list.append(ObjectId(item))
#     query_dict.update({"_id":{"$in":teacher_list},"_deleted":False})
#     teacher_list = list( Teacher.coll().find(query_dict))
#     #将class 里面的teacher 换成对应的instance
#     for item in teacher_list:
#         for index in range(len(list_temp)):
#             if item["_id"] ==  list_temp[index].get("teacherSrole"):
#                 list_temp[index]["teacherSrole"]=item
#                 pass
#
#
#     #统计每班的人数
#     for index in range(len(list_temp)):
#         studentCount = Student.coll().find({"class":ObjectId(list_temp[index]["_id"])}).count()
#         if studentCount == None:
#             studentCount=0
#
#         list_temp[index].update(studentCount=studentCount)
#
#     return objectIds_convert_json({"_items":list_temp})




def post_GET_classes(resource  , request,payload):
     #content_length
     #data
     # 1.
     # 找出lookup
     # 取出data.
     # 2.
     # 统计学生数量
     # 3.
     # 将数据存入data中
     # 4.
     # 修改
     # content_length
     # if lookup._status_code == 200 and resource == 'classStypes':

    if resource == 'classes' and payload._status_code == 200:


        _data = json.loads(payload.response[0].decode('utf-8'))
        '''
        1. 获取class_id
        2. 去数据库查
        3. 把数据更新到 payload.response[0]中.
        '''

        if _data.get("_items") != None:
            for index in range(len(_data.get("_items"))):
                item = _data.get("_items")[index]
                countStudent = Student.coll().find({"class":ObjectId(item.get("_id")),"_deleted":False}).count()
                if countStudent == None:
                    countStudent = 0
                _data.get("_items")[index].update(countStudent=countStudent)

            payload.response[0] = json.dumps(_data).encode("utf-8")
            payload.content_length = len(json.dumps(_data).encode("utf-8"))

def select_teachering_teacher(school_id,class_id):
    #class_id 是支持集合.
    result_list = request.json
    if type({}) == type(result_list):
        result_list=[result_list]
    class_ins = XG_Class.coll().find_one({
        "_deleted": False,
        "_id": ObjectId(class_id),
        "school":ObjectId(school_id)
    })
    if class_ins != None:
        #拿取 cls 的 teacherTrole 和 result_list 进行比较
        cls_t_role = class_ins.get("teacherTrole")
        new_list=[]
        for item in cls_t_role:
            for tmp in result_list:
                if tmp['discipline'] == item.get("discipline"):
                    if tmp['teacher']== None or Teacher.coll().find({"_deleted":False,"_id": ObjectId(tmp['teacher'])}) != None :
                        item = tmp
                    else:
                        return jsonify(_items="teacher不存在"),400
            new_list.append(item)
        XG_Class.coll().update({
            "_id" : class_ins["_id"]
        },{
            "$set":{
                "teacherTrole":new_list
            }
        })
        return jsonify(_items="success"),200
    return jsonify(_items="班级不存在.请重试"),404



def teacher_select_classes(school_id,teacher_id,cls_id):
    cls = cls_id.split(",")
    teacher_ins =Teacher.coll().find_one({
        "_deleted":False,
        "school":ObjectId(school_id),
        "_id":ObjectId(teacher_id)
    })
    cls_obj_list = [ObjectId(item)for item in cls]

    cls_ins =list(XG_Class.coll().find({"_deleted":False,"school":ObjectId(school_id),"_id":{"$in":cls_obj_list}}))

    for index in range(len(cls_ins)):
        tmp_list = cls_ins[index].get("teacherTrole")
        for idx in range(len(tmp_list)):
            if tmp_list[idx].get('discipline') == teacher_ins["primaryDiscipline"]:
                tmp_list[idx]["teacher"] = teacher_ins["_id"]
                cls_ins[index].get("teacherTrole")[idx]= tmp_list[idx]
                XG_Class.coll().update({
                    "_id":cls_ins[index].get("_id")
                },{
                    "$set":{
                        "teacherTrole":cls_ins[index].get("teacherTrole")
                    }
                })
                break
    return jsonify(_item="success"),200


#查询任课老师的
def query_teaching_teacher(request,payload):
    _data  = json.loads(payload.response[0].decode("utf-8"))
    if type(_data) == type({}) and _data.get("_items")==None:
        t_role_list = _data.get("teacherTrole")
        result_list = []

        for item in t_role_list:
            if item["teacher"] != None:
                teacher_ins = Teacher.coll().find_one({"_id": ObjectId(item['teacher'])})

                item['teacher'] = teacher_ins
            result_list.append(item)
        _data['teacherTrole'] = result_list
        payload.response[0] = my_dump(_data)
        payload.content_length = len(my_dump(_data))

    pass


def get_present_classes(request,lookup):
    query_dict = request.args.get("where")
    if query_dict!=None:
        present_cls = json.loads(query_dict)
        present = present_cls.get("present")
        if present == True :
            #进行筛选

            #获得有效年级
            school_id = re.search('[a-f0-9A-F]{24}', request.base_url).group()

            present_grade_list = [item['_id'] for item in get_grades_by_time(school_id, 0, 1)]
            _where =my_dump({
                "grade":{
                    "$in":present_grade_list
                }
            })
            args= request.args.to_dict()
            args["where"] = _where
            request.args = request.args.to_dict()
            if request.args.get("max_results") != None:
                args.upate(max_results=request.args.get("max_results"))
            if request.args.get("page") != None:
                args.upate(page=request.args.get("page"))

            request.args= args
            request.args= ImmutableMultiDict(request.args)
            pass
    pass


def set_class_grade_title(requets,payload):
    temp = payload.response[0]
    if type(temp)== type(""):
        _data = json.loads(temp)
    else:
        _data = json.loads(temp.decode('utf-8'))
    cls_list = _data.get("_items")
    if cls_list != None:
        cls_list_new = []
        for cls in cls_list:
            grade = cls.get("grade")
            if type(grade) == type({}):
                grade_ins  = Grade.coll().find_one({"_id":ObjectId(grade["_id"]),"_deleted":False})
                title = set_title_by_grade(arrow.get(grade_ins['birth']), arrow.utcnow())
                cls.update(gradeTitle=title)
            if type(grade) == type(""):
                grade_ins = Grade.coll().find_one({"_id": ObjectId(grade), "_deleted": False})
                title = set_title_by_grade(arrow.get(grade_ins['birth']), arrow.utcnow())
                cls.update(gradeTitle=title)

            cls_list_new.append(cls)

        _data.update(_items=cls_list_new)
        payload.response[0] = my_dump(_data)
        payload.content_length = len(my_dump(_data))

    pass