from flask import make_response
from flask import request
from flask import send_from_directory
from ms.hooks.req_addon import *
from ms.hooks.taginfo import *
from ms.models.ENUM import Enum
from ms.models.ROLE import Role
from sc.question_similarity.similar_check import get_similar


def question_summations(name):
    '''
    题目的统计信息
    :param id:
    :return:
    '''
    question = Question.coll()
    lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
    lookup = Question.parserargs(request,lookup)
    if "botn" in lookup:
        botn = lookup.pop("botn")
    data = list(question.find(lookup))
    info = summations(data,getczj_info(botn))
    response = jsonify({'_items': json.loads(my_dump(info))})
    return response


def batch_question_summations(name):
    '''
    题目的统计信息,batch（例如，获取某章下面所有的题目）
    :param id:
    :return:
    '''
    lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
    lookup = Question.parserargs(request,lookup)
    botnid = lookup.pop("botn")
    lookup =Role.authcheck("Get",lookup)
    sonward = ques_status(botnid)
    if not sonward:
        abort(404,description="botn has not found")
    col_question = Question.coll()
    if lookup.get("koDiscipline") == 'english':
        questions = list(col_question.find(lookup))
        fullstat = batch_stat_en(sonward,questions)
    else:  # 非英语学科
        questions = list(col_question.find(lookup))
        questions.sort(key=itemgetter('section'))
        ques = groupby(questions, itemgetter('section'))  # 将题目按节分类
        fullstat = []
        stats = []
        for k, v in ques:  # 节上的题目统计
            for j in sonward:
                if j.get('_id') == k:
                    data = summations(v, j)
                    stats.append(data)
                    continue
        [batch_stat(cat,stats,fullstat) for cat in sonward if cat.get("koLyro") == 'chapter']
        [batch_stat(cat,stats,fullstat) for cat in sonward if cat.get("koLyro") == 'volume']
        fullstat.extend(stats)
    response = jsonify({'_items':json.loads(my_dump(fullstat))})
    return response


def difficulty(name):
    '''
    author: cst
    difficult类型状态(难度统计)
    :param name:
    :return:
    '''
    enum = Enum.coll()
    question = Question.coll()
    Literal = ('QuestionDifficultyKind','difficulty')  ## enum里面保存的name和question里面的数据名称不一样,对照元祖
    lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
    lookup = Question.parserargs(request,lookup)
    if "botn" in lookup:
        lookup.pop("botn")
    data = list(question.find(lookup))
    tag = enum.find_one({"name":Literal[0]}).get('literal')
    res = partitions(data,tag,Literal)
    response = jsonify(res)
    return response


def multi_dimension(name):
    """
    多维统计包括了对各个标签的统计
    :param name:
    :return:
    """
    enum = Enum.coll()
    question = Question.coll()

    lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
    scope = json.loads(request.args.get('scope'))
    lookup = Question.parserargs(request,lookup)
    if "botn" in lookup:
        lookup.pop("botn")
    Literal = get_literal(scope)
    data = list(question.find(lookup))
    resdata = dict(count=len(data),partition=[])
    for Liter in Literal:
        tag = enum.find_one({"name": Liter[0]}).get('literal')
        tag = partitions(data,tag,Liter)
        res = dict(by=Liter[0],summations=tag)
        resdata['partition'].append(res)
    response = jsonify(resdata)
    return response


def material_kind(name):
    '''
    author: cst
    材料类型,语言类(英语)
    :param name: 资源库名称
    :return:
    '''
    enum = Enum.coll()
    question = Question.coll()
    Literal = ('QuestionMaterialKind','koMaterial')  ## enum里面保存的name和question里面的数据名称不一样,对照元祖
    lookup = {"quesBank":name,"dad":{"$exists":False},"_deleted":False}
    lookup = Question.parserargs(request, lookup)
    if "botn" in lookup:
        lookup.pop("botn")
    data = list(question.find(lookup))
    if "botn" in lookup:
        lookup.pop("botn")
    tag = enum.find_one({"name":Literal[0]}).get('literal')
    res = partitions(data,tag,Literal)
    response = jsonify(res)
    return response


def similar(name,id=None,limit=5):
    '''
    重题检测,指定id,查找和该题类似题，否则全库查找同科目的类似题目
    :param name:
    :return:
    '''
    '''重题算法'''
    col_question = Question.coll()
    data = list(col_question.find().limit(5))
    #还需要将题目的路径统计出来
    en_ques = [ques for ques in data if ques.get("koDiscipline") == "english"]
    oth_ques = [ques for ques in data if ques.get("koDiscipline") != "english"]
    # 英语学科的path为 [koDiscipline,volume,comboFormat]
    for ques in en_ques:
        vol_info = BOTNode.coll().find_one(ques.get("volume"))
        ques.update(bot_path=[
            getcombo_info(ques.get("koDiscipline"),name='ExampaperDisciplineKind').get("title"),
            vol_info.get("title"),
            getcombo_info(ques.get("comboFormat")).get("title")
        ])
    # 非英语学科path为 [koDiscipline,volume,chapter,section]
    for ques in oth_ques:
        sec_info = BOTNode.coll().find_one(ques.get("section"))
        chapte_info = BOTNode.coll().find_one(sec_info.get("dad"))
        vol_info = BOTNode.coll().find_one(chapte_info.get("dad"))
        ques.update(
            bot_path=[
            getcombo_info(ques.get("koDiscipline"), name='ExampaperDisciplineKind').get("title"),
            vol_info.get("title"),
            chapte_info.get("title"),
            sec_info.get("title")
        ])
    response =jsonify(json.loads(my_dump(dict(_items=data))))
    return response


def similar1(name,id=None,limit=5):
    '''
    重题检测,指定id,查找和该题类似题，否则全库查找同科目的类似题目
    :param name:
    :return:
    '''
    '''重题算法'''
    col_question = Question.coll()
    lookup = {}
    if id:
        content = col_question.find_one({"_id":ObjectId(id)}).get("contOfQuery")
        data = get_similar(content,lookup={"_id":{"$ne":ObjectId(id)}})
    else:
        content = request.args.get("contOfQuery","")
        _id = request.args.get("_id", None)
        if _id:
            lookup = {"_id": {"$ne": ObjectId(id)}}
        data = get_similar(content,lookup=lookup)
    #还需要将题目的路径统计出来
    en_ques = [ques for ques in data if ques.get("koDiscipline") == "english"]
    oth_ques = [ques for ques in data if ques.get("koDiscipline") != "english"]
    # 英语学科的path为 [koDiscipline,volume,comboFormat]
    for ques in en_ques:
        vol_info = BOTNode.coll().find_one(ques.get("volume"))
        ques.update(bot_path=[
            getcombo_info(ques.get("koDiscipline"),name='ExampaperDisciplineKind').get("title"),
            vol_info.get("title"),
            getcombo_info(ques.get("comboFormat")).get("title")
        ])
    # 非英语学科path为 [koDiscipline,volume,chapter,section]
    for ques in oth_ques:
        sec_info = BOTNode.coll().find_one(ques.get("section"))
        chapte_info = BOTNode.coll().find_one(sec_info.get("dad"))
        vol_info = BOTNode.coll().find_one(chapte_info.get("dad"))
        ques.update(
            bot_path=[
            getcombo_info(ques.get("koDiscipline"), name='ExampaperDisciplineKind').get("title"),
            vol_info.get("title"),
            chapte_info.get("title"),
            sec_info.get("title")
        ])
    response =jsonify(json.loads(my_dump(dict(_items=data))))
    return response


def stats(name):
    """
    资源库的数据统计(用户的录题，打标，审核量...)
    :param name: 题库名
    :return:
    """
    lookup = {'quesBank':name,'dad':{"$exists":False},'_deleted':False}
    scope,lookup = Question.jobargs(request,lookup)
    data,count = Question.jobstat(lookup,scope)
    # alt=csv 时需要将其导出为excel文件
    if scope.get("alt") == 'csv':
        data = json_to_excel(json.loads(my_dump(data)))
        directory = "/tmp"
        response = make_response(send_from_directory(directory, "output.xlsx", as_attachment=True))
        return response
    resp = dict(scope=scope,summations=data,count=count)
    response = jsonify(json.loads(my_dump(resp)))
    return response
