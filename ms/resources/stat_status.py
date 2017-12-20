from flask import make_response
from flask import request, g
from flask import send_from_directory

from ms.validators import MyValidator
from ms.hooks.req_addon import *
from ms.hooks.taginfo import *
from ms.models.ENUM import Enum
from ms.models.ROLE import Role


# def question_summations(name):
#     '''
#     题目的统计信息
#     :param id:
#     :return:
#     '''
#     # args = request.args
#     # scope = json.loads(args.get('scope'))
#     #
#     # discipline = scope.get('koDiscipline')
#     # botnid = scope.get('botn')
#     #
#     # sonward = ques_status(botnid)
#     # botn = getczj_info(botnid)
#     # if not sonward:
#     #     return jsonify(dict(info="botn has not found"))
#     # questions = query_question_stat(sonward,botn,discipline)
#     lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
#     lookup = Question.parserargs(request,lookup)
#     if "botn" in lookup:
#         botn = lookup.pop("botn")
#
#     question = Question.coll()
#     data = list(question.find(lookup))
#     info = summations(data,getczj_info(botn))
#     return jsonify({'_items':json.loads(my_dump(info))})
#
#
# # def batch_question_summations(name):
# #     '''
# #     题目的统计信息,batch
# #     :param id:
# #     :return:
# #     '''
# #     args = request.args
# #     scope = json.loads(args.get('scope'))
# #
# #     discipline = scope.get('koDiscipline')
# #     botnid = args.get('sonern-of')
# #
# #     sonward = ques_status(botnid)
# #     if not sonward:
# #         abort(404,description="botn has not found")
# #     questions = query_questions_stat(sonward,discipline)
# #     resp = jsonify({'_items':json.loads(my_dump(questions))})
# #     return resp
#
#
# def batch_question_summations(name):
#     '''
#     题目的统计信息,batch
#     :param id:
#     :return:
#     '''
#     lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
#     lookup = Question.parserargs(request,lookup)
#     botnid = lookup.pop("botn")
#     lookup =Role.authcheck("Get",lookup)
#
#     sonward = ques_status(botnid)
#     if not sonward:
#         abort(404,description="botn has not found")
#     col_question = Question.coll()
#     if lookup.get("koDiscipline") == 'english':
#         questions = list(col_question.find(lookup))
#         fullstat = batch_stat_en(sonward,questions)
#     else:  # 非英语学科
#         questions = list(col_question.find(lookup))
#         questions.sort(key=itemgetter('section'))
#         ques = groupby(questions, itemgetter('section'))  # 将题目按节分类
#         fullstat = []
#         stats = []
#         for k, v in ques:  # 节上的题目统计
#             for j in sonward:
#                 if j.get('_id') == k:
#                     data = summations(v, j)
#                     stats.append(data)
#                     continue
#         # for cat in sonward:
#         #     if cat.get('koLyro') == 'chapter':
#         #         batch_stat(cat, stats, fullstat)
#         # for cat in sonward:
#         #     if cat.get('koLyro') == 'volume':
#         #         batch_stat(cat, fullstat, fullstat)
#         [batch_stat(cat,stats,fullstat) for cat in sonward if cat.get("koLyro") == 'chapter']
#         [batch_stat(cat,stats,fullstat) for cat in sonward if cat.get("koLyro") == 'volume']
#         fullstat.extend(stats)
#
#     resp = jsonify({'_items':json.loads(my_dump(fullstat))})
#     return resp
#
#
#
#
#
#
# def difficulty(name):
#     '''
#     author: cst
#     difficult类型状态d
#     :param name:
#     :return:
#     '''
#     Literal = ('QuestionDifficultyKind','difficulty')  ## enum里面保存的name和question里面的数据名称不一样,对照元祖
#
#     lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
#     lookup = Question.parserargs(request,lookup)
#     if "botn" in lookup:
#         lookup.pop("botn")
#
#     question = Question.coll()
#     data = list(question.find(lookup))
#
#     enum = Enum.coll()
#     tag = enum.find_one({"name":Literal[0]}).get('literal')
#     res = partitions(data,tag,Literal)
#     resp = jsonify(res)
#     return resp
#
#
# def multi_dimension(name):
#     lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
#
#     scope = json.loads(request.args.get('scope'))
#     lookup = Question.parserargs(request,lookup)
#     if "botn" in lookup:
#         lookup.pop("botn")
#
#     Literal = get_literal(scope)
#
#     question = Question.coll()
#     data = list(question.find(lookup))
#     resdata = dict(
#         count=len(data),
#         partition=[]
#     )
#     enum = Enum.coll()
#
#     for Liter in Literal:
#         tag = enum.find_one({"name": Liter[0]}).get('literal')
#         # res = partitions_dimension(data, tag, Liter)
#         tag = partitions(data,tag,Liter)
#         res = dict(by=Liter[0],summations=tag)
#         resdata['partition'].append(res)
#     resp = jsonify(resdata)
#     return resp
#
#
# def material_kind(name):
#     '''
#     author: cst
#     材料类型,语言类(英语)
#     :param name:
#     :return:
#     '''
#     Literal = ('QuestionMaterialKind','koMaterial')  ## enum里面保存的name和question里面的数据名称不一样,对照元祖
#     lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
#     lookup = Question.parserargs(request, lookup)
#     if "botn" in lookup:
#         lookup.pop("botn")
#     # args = request.args
#     # scope = args.get('scope')
#     # if scope:  # scope 控制范围,如果没有这个参数默认查询name题库下所有
#     #     lookup.update(json.loads(args.get('scope')))
#     #     volumes = []
#     #     if 'botn' in json.loads(scope):
#     #         botnid = json.loads(scope).get('botn')
#     #         recursion_structuring(botnid,volumes,BOTNode.coll())
#     #         vid = [i.get('_id') for i in volumes if i.get('koLyro') == 'volume']
#     #         lookup.update({"$or": [{"volume": {"$in": vid}}]})
#     #         lookup.pop('botn')
#     question = Question.coll()
#     data = list(question.find(lookup))
#     if "botn" in lookup:
#         lookup.pop("botn")
#
#     enum = Enum.coll()
#     tag = enum.find_one({"name":Literal[0]}).get('literal')
#     res = partitions(data,tag,Literal)
#     resp = jsonify(res)
#     return resp
#
#
# # def batch_question_summations(name):
# #     '''
# #     author: cst
# #     批量统计某册或章节下面所有子章节所有的统计状态信息
# #     :param name:
# #     :return:
# #     '''
# #     lookup = {"quesBank":name}
# #     discipline = ''
# #     args = request.args
# #
# #     if args.get('scope'):  # scope 控制范围,如果没有这个参数默认查询name题库下所有
# #         scope = json.loads(args.get('scope'))
# #         lookup.update(scope)
# #
# #     sonern = args.get('sonern-of')
# #     if sonern:
# #         botn = BOTNode.coll()
# #         bot = botn.find_one({'_id': ObjectId(sonern)}, {"name": 1, "title": 1, "koLyro": 1})
# #         if bot:
# #             Lyro = bot.get("koLyro")
# #             type = {Lyro:sonern}
# #     lookup.update(type)
# #     if lookup.get('koDiscipline') == 'english':
# #         discipline = 'english'
# #
# #     question = Question.coll()
# #     data = list(question.find(lookup))
# #     res = batch_summations(data,type,bot,discipline)
# #     resp = jsonify(res)
# #     return resp
# #
# #
# # def question_summations(name):
# #     '''
# #     author: cst
# #     统计某章下面的节所有的统计状态信息
# #     :param name:
# #     :return:
# #     '''
# #     lookup = {"quesBank":name}
# #     args = request.args
# #     if args.get('scope'):  # scope 控制范围,如果没有这个参数默认查询name题库下所有
# #         scope = json.loads(args.get('scope'))
# #         if 'botn' in scope:
# #             botnId = scope.pop('botn')
# #             botn = BOTNode.coll()
# #             bot = botn.find_one({'_id':ObjectId(botnId)},{"name":1,"title":1,"koLyro":1})
# #             if bot:
# #                 Lyro = bot.get("koLyro")
# #                 scope.update({Lyro:botnId})
# #         lookup.update(scope)
# #     question = Question.coll()
# #     data = question.find(lookup)
# #     res = summations(data,bot)
# #     resp = jsonify(res)
# #     return resp
#
# def similar(name,id=None,limit=5):
#     '''
#     重题检测,指定id,查找和该题类似题，否则全库查找同科目的类似题目
#     :param name:
#     :return:
#     '''
#     '''重题算法'''
#     col_question = Question.coll()
#     data = list(col_question.find().limit(5))
#     #还需要将题目的路径统计出来
#     en_ques = [ques for ques in data if ques.get("koDiscipline") == "english"]
#     oth_ques = [ques for ques in data if ques.get("koDiscipline") != "english"]
#     # 英语学科的path为 [koDiscipline,volume,comboFormat]
#     for ques in en_ques:
#         vol_info = BOTNode.coll().find_one(ques.get("volume"))
#         ques.update(bot_path=[
#             getcombo_info(ques.get("koDiscipline"),name='ExampaperDisciplineKind').get("title"),
#             vol_info.get("title"),
#             getcombo_info(ques.get("comboFormat")).get("title")
#         ])
#     # 非英语学科path为 [koDiscipline,volume,chapter,section]
#     for ques in oth_ques:
#         sec_info = BOTNode.coll().find_one(ques.get("section"))
#         chapte_info = BOTNode.coll().find_one(sec_info.get("dad"))
#         vol_info = BOTNode.coll().find_one(chapte_info.get("dad"))
#         ques.update(
#             bot_path=[
#             getcombo_info(ques.get("koDiscipline"), name='ExampaperDisciplineKind').get("title"),
#             vol_info.get("title"),
#             chapte_info.get("title"),
#             sec_info.get("title")
#         ])
#     resp =jsonify(json.loads(my_dump(dict(_items=data))))
#     return resp
#
#
# def stats(name):
#     lookup = {'quesBank':name,'dad':{"$exists":False},'_deleted':False}
#     scope,lookup = Question.jobargs(request,lookup)
#     data,count = Question.jobstat(lookup,scope)
#     # if scope.get("alt") == 'csv':
#     #     #data = json_to_csv(json.loads(my_dump(data)))
#     #     data = json_to_csv(json.loads(my_dump(data)))
#     #     response = make_response(data)
#     #     response.headers["Content-Type"] = "text/csv"
#     #     response.headers["Content-Disposition"] = "attachment; filename=statistic.csv"
#     #     return response
#     #     pass # todo export csv file
#     if scope.get("alt") == 'csv':
#         #data = json_to_csv(json.loads(my_dump(data)))
#         data = json_to_excel(json.loads(my_dump(data)))
#         directory = "/tmp"
#         response = make_response(send_from_directory(directory, "output.xlsx", as_attachment=True))
#         return response
#
#     else:
#         resp = dict(
#             scope=scope,
#             summations=data,
#             count=count
#         )
#         resp = jsonify(json.loads(my_dump(resp)))
#         return resp

def tag(name):
    ques = request.json
    question = Question.coll()
    tag_stat = []
    for que in ques:
        id = que.get('_id')
        taginfo = que.get('taginfo')
        boknCat = taginfo.get("boknCat")
        lookup = {'quesBank':name,'_id':ObjectId(id)}
        quest = question.find_one(lookup)
        if not quest:
            tag_stat.append(dict(
                id=id,
                status='question not found'
            ))
            continue
        if not quest.get("taggedAtFirstly"):
            taginfo.update(dict(
                taggedAtFirstly=datetime.now(),
                taggedByFirstly=g.user.get("_id") # 通过token解析出来的
            ))
        if quest.get("dad"):
            questdd = question.find_one({'quesBank':name,'_id':quest.get("dad")})
            code = Role.authcheck("Tag", questdd)
        else:
            code = Role.authcheck("Tag",quest)
        if code == 403:
            tag_stat.append(dict(
                id=id,
                status='tag is forbiden'
            ))
            continue
        taginfo.update(dict(taggedAtLastly=datetime.now()))
        if boknCat:
            if isinstance(boknCat, str):
                boknCat = [boknCat]
            v = MyValidator()
            bokinfo = v._validate_type_boknpid(boknCat)
            if not bokinfo:
                tag_stat.append(dict(
                    id=id,
                    status='boknCat must be of boknpid type'
                ))
                continue
            boknCat = v._normalize_coerce_distbok(boknCat)
            taginfo['boknCat'] = boknCat
        if quest.get("dad"):
            state = Question.on_signal(quest.get("dad"), 'tagged')
            if state in [1, 2, 3, 4]:
                question.update({'quesBank': name, '_id': quest.get("dad")}, {"$set": {"state": state}})
        else:
            question.update(lookup, {"$set": {"state": state}})
        upinfo = question.update(lookup,{"$set":taginfo})

        tag_stat.append(dict(id=id,
                    status= 'ok' if upinfo.get('ok') and upinfo.get('nModified') else 'error')
                    )
    return jsonify(dict(_items=tag_stat))


def tagging(para):
    """

    :param name:     quesbankname
    :param quest:    tag message
    :param question: collection
    :return:
    """
    name, quest, question = para
    id = quest.get('_id')
    taginfo = quest.get('taginfo',{})
    boknCat = taginfo.get("boknCat")
    lookup = {'quesBank':name,'_id':ObjectId(id)}
    quest = question.find_one(lookup)
    if not quest:
        resp = dict(id=id,status='question not found')
        return resp

    if not quest.get("taggedAtFirstly"):
        taginfo.update(dict(
            taggedAtFirstly=datetime.now(),
            taggedByFirstly=g.user.get("_id") # 通过token解析出来的
        ))

    if boknCat:
        if isinstance(boknCat, str):
            boknCat = [boknCat]
        v = MyValidator()
        bokinfo = v._validate_type_boknpid(boknCat)
        if not bokinfo:
            resp = dict(id=id,status='boknCat must be of boknpid type')
            return resp
        boknCat = v._normalize_coerce_distbok(boknCat)
        taginfo['boknCat'] = boknCat

    if quest.get("dad"):
        questdd = question.find_one({'quesBank':name,'_id':quest.get("dad")})
        code = Role.authcheck("Tag", questdd)
        if code == 403:
            resp = dict(id=id, status='tag is forbiden')
            return resp
        state = Question.on_signal(quest.get("dad"), 'tagged')
        if state in [1, 2, 3, 4]:
            question.update({'quesBank': name, '_id': quest.get("dad")}, {"$set": {"state": state}})
    else:
        code = Role.authcheck("Tag",quest)
        if code == 403:
            resp = dict(id=id, status='tag is forbiden')
            return resp
        state = Question.on_signal(id, 'tagged')
        if state in [1,2,3,4]:
            question.update(lookup, {"$set": {"state": state}})

    taginfo.update(dict(taggedAtLastly=datetime.now()))
    upinfo = question.update(lookup,{"$set":taginfo})

    resp = dict(id=id,status= 'ok' if upinfo.get('ok') and upinfo.get('nModified') else 'error')
    return resp


def tag2(name):
    quest_tag = request.json
    question = Question.coll()
    if isinstance(quest_tag,dict):
        para = (name, quest_tag, question)
        resp = tagging(para)
    if isinstance(quest_tag,list):
        para = ((name,tag,question) for tag in quest_tag)
        resp = list(map(tagging,para))
    return jsonify(dict(_items=resp))