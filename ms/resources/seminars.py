import arrow
import json
import re

from bson import ObjectId
from werkzeug.exceptions import abort

from ms.models.Seminar import Seminar
from ms.models.SeminarSpans import SeminarSpans

#
def post_POST_seminar_insert_seminarSpans_spans(request, payload):
    seminarSpans_id = request.view_args.get("seminarSpans")
    seminarSpans_ins = SeminarSpans.coll().find_one({
        "_id": ObjectId(seminarSpans_id)
    })
    if seminarSpans_ins == None:
        abort(400,'学期集不存在')

    spans_list = seminarSpans_ins.get("spans")
    if spans_list ==None:
        spans_list=[]
    _data = payload.response[0]
    if type(_data) != type(""):
        data = json.loads(_data.decode("utf-8"))
    else:
        data = json.loads(_data)
    spans_list.append(data.get("_id"))

    SeminarSpans.coll().update({
        "_id":seminarSpans_ins["_id"]
    },{
        "$set":{
            "spans":spans_list
        }
    })

    pass


def pre_post_seminars_validate_time(request):
    seminarSpan_id = request.view_args.get("seminarSpans")
#     选出所有的学期
#     找出最大的
#     end
#     然后和
#     传入的start
#     进行比较.
#     如果相等:
#     放行
# 如果不相等:
# 返回400.学期集不连续.
    seminar_ins_list = list(Seminar.coll().find({
        "seminarSpans":ObjectId(seminarSpan_id)
    }))
    if seminar_ins_list != []:

        max_endTime = arrow.get(seminar_ins_list[0].get("end"))
        for item in seminar_ins_list:
            end = arrow.get(item['end'])
            if end > max_endTime:
                max_endTime = end

        post_end_time = arrow.get(request.json.get("end"))
        post_start_time = arrow.get(request.json.get('start'))
        if post_end_time < post_start_time:
            abort(400, '学期时间不符合要求.')
        if post_start_time != max_endTime:
            abort(400,'学期时间不连续.')



    pass