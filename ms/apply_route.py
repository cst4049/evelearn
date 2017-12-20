from ms.app import app
from ms.resources import bok, burtree_node, signals, \
    stat_status, token_resource, users_resource
from ms.resources import move
from ms.resources.student import student_moveTo_class, pre_POST_students
from ms.resources.classes import select_teachering_teacher, teacher_select_classes
from ms import statistics


# also can work like this
@app.route('/heartbeat')
def heartbeat():
    return "I'm alive"



app.add_url_rule('/tokens','token', token_resource.check_token,
                 methods=['GET','POST'])

app.add_url_rule("/wordlists-commit","word_list_bokn", bok.english_word_list_insert,
                 methods=["POST"])

app.add_url_rule('/users/<user_id>/passwd','users', users_resource.change_passwd,
                 methods=['PATCH','GET']
                 )

app.add_url_rule('/<burtree_node_type>-nodes/<id>/<suffix>','burtreeNode', burtree_node.burrtree_son, methods=['GET'])

# app.add_url_rule('/aa/<id>','aa',signals.aa,methods=['GET'])

#checkT: 审核类型录入审核 打标审核
#signal: 信号类型 通过 拒绝 重置
app.add_url_rule('/quesbanks/<name>/questions/<id>/<regex("check-(typewrite|tag)-(pass|deny|reset)"):signal>',
                 'signal', signals.signal, methods=['POST']
                 )

app.add_url_rule('/quesbanks/<name>/question-partitions/by-difficulty/',
                 'difficulty', statistics.difficulty,
                 methods=['GET']
                 )

app.add_url_rule('/quesbanks/<name>/question-partitions/by-multi-dimension/',
                 'multi_dimension', statistics.multi_dimension,
                 methods=['GET']
                 )

app.add_url_rule('/quesbanks/<name>/question-partitions/by-material-kind/',
                 'material_kind', statistics.material_kind,
                 methods=['GET']
                 )

app.add_url_rule('/quesbanks/<name>/question-summations/batch-tagged-checked-all/',
                 'batch_question_summations', statistics.batch_question_summations,
                 methods=['GET']
                 )
#app.add_url_rule('/quesbanks/<name>/question-summations/batch-tagged-checked-all/',
# 'batch_question_summations',
# stat_status.batch_question_summations,
# methods=['GET'])

app.add_url_rule('/quesbanks/<name>/question-summations/tagged-checked-all/',
                 'question_summations', statistics.question_summations,
                 methods=['GET']
                 )
#app.add_url_rule('/quesbanks/<name>/question-summations/tagged-checked-all/',
# 'question_summations',stat_status.question_summations,
# methods=['GET']) old题目上挂有卷章信息

app.add_url_rule('/quesbanks/<name>/questions/<id>/similar',
                 'similar1', statistics.similar1,
                 methods=['GET']
                 )

app.add_url_rule('/quesbanks/<name>/questions/similar',
                 'similar1', statistics.similar1,
                 methods=['GET']
                 )

app.add_url_rule('/quesbanks/<name>/questions/tagging',
                 'tag', stat_status.tag2,
                 methods=['PATCH']
                 )

app.add_url_rule('/quesbanks/<name>/bulk:questions/',
                 'move',
                 move.move,
                 methods=['PATCH']
                 )

app.add_url_rule('/quesbanks/<name>/job-stats/res-per-user-typed-tagged-checked',
                 'res-per-user',
                 statistics.stats,
                 methods=['GET']
                 )





app.add_url_rule('/schools/<school_id>/classes/<class_src>/students/<student>/class/<class_target>',
                 'student_move',
                 student_moveTo_class,
                 methods=['PATCH']
                 )

# 选择授课老师
app.add_url_rule('/schools/<school_id>/classes/<class_id>/teacherTroles',
                 'classes',select_teachering_teacher,methods=['PATCH','PUT']
                 )

# 老师批量授课
app.add_url_rule('/schools/<school_id>/teachers/<teacher_id>/classes/<cls_id>',
                 'teacher_classes',teacher_select_classes,methods=['PUT','PATCH']
                 )

app.add_url_rule('/quesbanks/<name>/questions/<id>/',
                 'signal_test', signals.signaltest, methods=['SPUR']
                 )

app.add_url_rule('/schools/<school_id>/classes/<class_id>/students',
                 'import_student',pre_POST_students,methods=['POST']
                 )