import json
import os

import xlrd
from bson import ObjectId
from flask import jsonify
from ms.models.XG_Class import XG_Class
from werkzeug.datastructures import FileStorage

from ms.models.Student import Student


# def student_moveTo_class_demo():
#     args = request.args
#     src = json.loads(args.get("src"))
#     target = json.loads(args.get("target"))
#     query_dict= {}
#     query_dict.update(_id=ObjectId(target.get("classid")))
#     query_dict.update(_deleted=False)
#     cls = XG_Class.coll().find_one(query_dict)
# 
# 
#     query_dict.clear()
#     temp_student_list = []
#     for item in src.get("id"):
#         temp_student_list.append(ObjectId(item))
#     query_dict.update(_id={"$in":temp_student_list})
#     query_dict.update(_deleted=False)
# 
#     studentCount = Student.coll().find(query_dict).count()
#     if cls != None and studentCount == len(list(src.get("id"))):
#         query_dict.clear()
#         query_dict.update(_id={"$in":temp_student_list})
#         query_dict.update(_deleted=False)
#         a =Student.coll().update(query_dict,{"$set":{"class":cls["_id"]}},upsert=False,multi=True)
#         return jsonify(),200
#     return jsonify({"_items":"参数不正确"}),400
#     pass




#转班接口
def student_moveTo_class(school_id,class_src,student,class_target):
    if students_switch_class(school_id,class_src,student,class_target):
        return jsonify(_tems="success"),200
    return jsonify(_tems={"errorMsg":"可能是 班级,学生已失效"}),400



#关键字查询
def pre_GET_students(request,lookup):
    query_keyword = request.args.get("where")
    if query_keyword != None:
        _keyword = json.loads(query_keyword)
        keyword = _keyword.get("keyword")
        if keyword != None:
            request.args = request.args.to_dict()
            _where = json.dumps({"$or":[{"codeDtype":keyword},{"name":keyword}]})
            request.args.update(where=_where)
    pass


#转班逻辑
def students_switch_class(school_id,class_src,student,class_target,):
    # 校验 目标班级
    query_dict = {}
    query_dict.update(school=ObjectId(school_id))
    query_dict.update(_id=ObjectId(class_target))
    query_dict.update(_deleted=False)
    taget_cls = XG_Class.coll().find_one(query_dict)

    # 校验 源班级
    query_dict.clear()
    query_dict.update(school=ObjectId(school_id))
    query_dict.update(_id=ObjectId(class_src))
    query_dict.update(_deleted=False)
    src_cls = XG_Class.coll().find_one(query_dict)

    # 校验 学生.
    stu_list = student.split(",")
    stu_id_list = [ObjectId(item) for item in stu_list]
    query_dict.clear()
    query_dict.update(_id={"$in": stu_id_list})
    query_dict.update(_deleted=False)
    stu_ins_list = list(Student.coll().find(query_dict))

    if taget_cls != None and src_cls != None and len(stu_list) == len(stu_ins_list):
        # 更新操作.
        Student.coll().update(
            {
                "class": src_cls["_id"],
                "_id": {
                    "$in": stu_id_list
                }
            }, {
                "$set": {
                    "class": taget_cls["_id"]
                }
            }, multi=True
        )
        return True
    return False


def pre_POST_students(request):

    # file = xlrd.open_workbook()
    file = FileStorage(request.files.get("file"))

    #判断 有则使用

    #判断 无则创建
    path = "./temp"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    file_path = path + "/temp.execl"
    file.save(file_path)
    excel_ins = xlrd.open_workbook(file_path)
    table = excel_ins.sheets()[0]
    obj_list = []
    # for index in range(table.nrows-1):
    for index in range(1):
        row_ins = table.row_values(index+1)
        name =  row_ins[0]
        codeDtype = row_ins[1]
        sex = row_ins[2]
        if sex == '男':
            sex = "mela"
        elif sex == '女':
            sex = 'famele'
        else:
             sex = 'unspecified'

        if row_ins[3] =='':
            userStatus = "active"
        else:
            userStatus = row_ins[3]
        temp_dict = {}
        temp_dict.update(sex=sex)
        temp_dict.update(name=name)
        temp_dict.update(codeDtype=codeDtype)
        temp_dict.update(userStatus=userStatus)
        obj_list.append(temp_dict)
    # request._parsed_content_type =('application/json',{})
    # request.content_type = 'application/json'

    # request.files = ImmutableMultiDict()
    # request.data = my_dump(obj_list)



