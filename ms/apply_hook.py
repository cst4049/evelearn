
from ms.hooks import before_request
from ms.hooks.bok import post_POST_bokt, post_POST_bokn_son
from ms.hooks.bot import post_POST_bott
from ms.hooks.query_cache import cache_interceptor, set_cache
from ms.hooks.req_addon import *
from ms.models.pictures import post_POST_pictures
from ms.models.questions import *
from ms.resources.grade import pre_POST_grade_normalized_birth, post_GET_grade_select_grades_by_time
from ms.resources.questions import *
from ms.resources.seminars import post_POST_seminar_insert_seminarSpans_spans, pre_post_seminars_validate_time
from ms.resources.seminarspans import post_PATCH_seminarspans_insert_activeTime
from ms.resources.student import pre_GET_students
from ms.resources.teacher import post_GET_teachers_append_classTeached
from ms.resources.classes import post_GET_classes, \
    query_teaching_teacher, get_present_classes, set_class_grade_title

from ms.app import app

app.on_pre_GET += pre_GET
app.on_pre_GET_questions += pre_get_questions
app.on_pre_PATCH += pre_PATCH
app.on_pre_PATCH_questions += pre_patch_questions
app.on_pre_PUT += pre_PUT
app.on_pre_POST += pre_POST
app.on_pre_POST_questions += pre_post_questions
app.on_pre_DELETE += pre_DELETE
app.on_pre_DELETE_questions += pre_delete_questions
app.on_post_GET += post_GET
app.on_post_PATCH += post_PATCH
app.on_post_PUT += post_PUT
app.on_post_POST += post_POST_pictures

# bott 资源钩子
app.on_post_POST += post_POST_bott
app.on_post_POST += post_POST_bokt
app.on_post_DELETE += post_DELETE

# bokn 资源hook
app.on_post_POST_bokn_son += post_POST_bokn_son

# grade 资源钩子
# app.on_pre_POST_grades += pre_POST_grade_normalized_birth
app.on_post_GET_grades += post_GET_grade_select_grades_by_time


# class 资源hook
app.on_post_GET += post_GET_classes
app.on_post_GET_classes += query_teaching_teacher
app.on_pre_GET_classes += get_present_classes
app.on_post_GET_classes += set_class_grade_title
# teacher 资源hook 查询授课班级
app.on_post_GET_teachers += post_GET_teachers_append_classTeached

# student 资源钩子
app.on_pre_GET_students += pre_GET_students
# app.on_pre_POST_students += pre_POST_students



app.on_fetched_resource_questions += before_returning_questions
app.on_fetched_item_questions += before_returning_question
app.on_insert_questions += before_insert_question
app.on_update_questions += before_update_question2
app.on_inserted_questions += after_inserted_questions


#seminar hook
app.on_post_POST_seminars += post_POST_seminar_insert_seminarSpans_spans
app.on_post_PATCH_seminarSpans += post_PATCH_seminarspans_insert_activeTime
app.on_pre_POST_seminars += pre_post_seminars_validate_time


app.before_request(before_request.interpretor)
app.before_request(before_request.delay) # 在所有请求前调用该函数
app.before_request(before_request.record)

#新增缓存
app.before_request(cache_interceptor)
app.after_request(set_cache)