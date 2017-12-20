import json
import re

import arrow
from bson import ObjectId

from ms.models.Grade import Grade
from ms.resources.unit import my_dump


def pre_POST_grade_normalized_birth(lookup):
    birth = lookup.json.get("birth")
    if birth != None:
        lookup.json.update(birth=normalize_grade_birth(birth))

#对齐到0点
def normalize_grade_birth(value):
    birth = value
    if birth != None:
        #进行格式转换,
        time_temp = arrow.get(birth)
        temp = time_temp.replace(hour=0,minute=0,second=0)
        return temp.datetime
    return value




#选出所有的grade. 然后对grade做一次筛选.
def post_GET_grade_select_grades_by_time(request, payload):
    school_id = re.search('[a-f0-9A-F]{24}', request.base_url).group()

    #1.筛选满足条件的grade
    _args = request.args.get("sel")
    _where = request.args.get("where")
    if _where != None:
        if json.loads(_where).get("present") ==True:
            result_list = get_grades_by_time(school_id, 0, 1)
            query_dict={}
            query_dict.update(_items=result_list)
            payload.response[0] = my_dump(query_dict)
            payload.content_length = len(my_dump(query_dict))
            pass
    if _args != None:
        args = json.loads(_args)
        _past = args.get("past")
        _future = args.get("future")

        if _past != None:
            past = int(_past)
        else:
            past = 0

        if _future != None:
            future = int(_future)
        else:
            future = 0
        result_list = get_grades_by_time(school_id, past, future)


        query_dict={}
        query_dict.update(_items=result_list)
        payload.response[0] = my_dump(query_dict)
        payload.content_length = len(my_dump(query_dict))
        pass





def get_grades_by_time(school_id, past, future):
    """
    查出这个学校的所有年级, 根据年级添加title: 高一 高二 高三 还是 往届
    :param school_id:
    :param past:
    :param future:
    :return:
    """
    query_dict = {}
    query_dict.update(_deleted=False)
    query_dict.update(school=ObjectId(school_id))

    _grade_list = list(Grade.coll().find(query_dict))
    now_time = arrow.utcnow().replace(hour=0, minute=0, second=0, years=-(3 + past))
    grade_list = []
    for item in _grade_list:
        grade_birth = arrow.get(item['birth'])
        if now_time < grade_birth and grade_birth < arrow.utcnow().replace(years=+future):
            grade_list.append(item)
    # 2.添加title
    result_list = []
    for item in grade_list:
        grade_birth = arrow.get(item['birth'])
        now_time = arrow.utcnow().replace(hour=0, minute=0, second=0)
        item.update(title=set_title_by_grade(grade_birth, now_time))

        # if now_time < grade_birth:
        #     item.update(title=(str(grade_birth.year) + "级"))
        # elif now_time.replace(hour=0, minute=0, second=0, years=-1) < grade_birth:
        #     item.update(title="高一")
        # elif now_time.replace(hour=0, minute=0, second=0, years=-2) < grade_birth:
        #     item.update(title="高二")
        # elif now_time.replace(hour=0, minute=0, second=0, years=-3) < grade_birth:
        #     item.update(title="高三")
        # else:
        #     item.update(title=(str(grade_birth.year + 3) + "届"))
        result_list.append(item)
    return result_list


#传入的时间是 arrow对象
def set_title_by_grade(target_time, basis):
    target_time = target_time.replace(hour=0, minute=0, second=0)
    if basis < target_time:
        title = str(target_time.year) + "级"
    elif basis.replace(hour=0, minute=0, second=0, years=-1) < target_time:
        title="高一"
    elif basis.replace(hour=0, minute=0, second=0, years=-2) < target_time:
        title="高二"
    elif basis.replace(hour=0, minute=0, second=0, years=-3) < target_time:
        title="高三"
    else:
        title = str(target_time.year+3) + "届"

    return title
