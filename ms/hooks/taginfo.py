from itertools import groupby
from operator import itemgetter

from ms.models.BOT import BOTNode
from ms.models.ENUM import Enum
from ms.models.Question import Question
from ms.resources.unit import *


def getczj_info(id):
    botn = BOTNode.coll()
    bot = botn.find_one({'_id': ObjectId(id)}, {"name": 1, "title": 1, "koLyro": 1})
    if bot:
        return bot


def getcombo_info(combo,name='EnglishQuestionComboFormatKind'):
    '''
    获取枚举字段的信息(复合形式的具体信息)
    :param combo:
    :return:
    '''
    enum = Enum.coll()
    bot = enum.find_one({'name': name}, {"literal": 1,'_id':0})
    if bot.get('literal'):
        for i in bot.get('literal'):
            if i.get('name') == combo:
                return i


def getson_ques(lookup):
    """get son quest"""
    quest = Question.coll()
    bot = quest.find_one(lookup, {"son":1})
    if bot:
        return bot


def summations(data,bot):
    '''
    只统计单个节点下的统计数
    :param data:
    :return:
    '''
    state_1, state_2, state_3,state_4,count = 0,0,0,0,0
    for quest in data:
        count += 1
        if quest.get("state") == 1:
            state_1 += 1
        if quest.get('state') == 2:
            state_2 += 1
        if quest.get("state") == 3:
            state_3 += 1
        if quest.get('state') == 4:
            state_4 += 1
    resdata = dict(
        count=count,
        summations=[
            dict(
                criteria="state_1",
                count=state_1
            ),
            dict(
                criteria="state_2",
                count=state_2
            ),
            dict(
                criterial="state_3",
                count=state_3
            ),
            dict(
                criteria="state_4",
                count=state_4
            )
        ]
    )
    if "_id" in bot:
        bot=dict(
            _id=str(bot.get('_id')),
            name=bot.get('name'),
            title=bot.get('title')
       )
    resdata.update(scope=bot)
    return resdata


# def summations_english(data,bot):
#     '''
#     只统计单个节点下的统计数
#     :param data:
#     :return:
#     '''
#     count, tagged, checked = 0,0,0
#     for quest in data:
#         count += 1
#         if 'tag' in quest:
#             tagged += 1
#         if quest.get('statusOfCheck') == 'pass':
#             checked += 1
#     resdata = {
#         'count': count,
#         'scope':bot,
#         'summations':[
#             {
#                 "criteria": "tagged",
#                 "count": tagged
#             },
#             {
#                 "criteria": "checked",
#                 "count": checked
#             },
#             {
#                 "criterial": "all",
#                 "count": count
#             }
#         ]
#     }
#     return resdata


# def batch_summations(data,botn,bot,discipline):
#     '''
#     批量统计以下各节点的题目统计数(统计是基于题目上有具体的章节信息)
#     :param data:
#     :param botn:
#     :return:
#     '''
#     respdata = {}
#     if 'volume' in botn:
#         if discipline == "english":
#             respdata.update({bot.get('name'): summations(data,bot)})
#             resp_chapter = (i for i in data if "comboFormat" in i)
#             chapters = groupby(resp_chapter, itemgetter('comboFormat'))
#             for key,groups in chapters:
#                 bot_son = getcombo_info(key)
#                 respdata.update({key:summations_english(groups,bot_son)})
#         else:
#             respdata.update({bot.get('name'): summations(data,bot)})
#             resp_chapter = (i for i in data if "chapter" in i)
#             chapters = groupby(resp_chapter, itemgetter('chapter'))
#             for key, groups in chapters:
#                 bot_son = getczj_info(key)
#                 respdata.update({bot_son.get('name'): summations(groups,bot_son)})
#             resp_section = (i for i in data if "section" in i)
#             sections = groupby(resp_section, itemgetter('section'))
#             for key, groups in sections:
#                 bot_son = getczj_info(key)
#                 respdata.update({bot_son.get('name'): summations(groups,bot_son)})
#     elif list(botn.keys())[0] == 'chapter':
#         resp_chapter = (i for i in data if "chapter" in i)
#         chapters = groupby(resp_chapter, itemgetter('chapter'))
#         for key, groups in chapters:
#             respdata.update({bot.get('name'):summations(groups,bot)})
#         resp_section = (i for i in data if "section" in i)
#         sections = groupby(resp_section, itemgetter('section'))
#         for key, groups in sections:
#             bot_son = getczj_info(key)
#             respdata.update({bot_son.get('name'): summations(groups, bot_son)})
#     elif list(botn.keys())[0] == 'section':
#         resp_section = (i for i in data if "section" in i)
#         sections = groupby(resp_section, itemgetter('section'))
#         for key, groups in sections:
#             bot_son = getczj_info(key)
#             respdata.update({bot_son.get('name'): summations(groups, bot_son)})
#     else:
#         raise ValueError
#     return respdata


def partitions(data,tag,Literal):
    '''
    author: cst
    数据统计,统计每个标签的题目
    :param data:
    :param tag:
    :param Literal:
    :return:
    '''
    count = 0
    _tag = [i.update(count=0) for i in tag] # 先添加count字段到tag中
    for quest in data:
        count += 1
        for i in tag:
            if quest.get(Literal[1]) == i.get('name'):
                i['count'] += 1
    resdata = dict(
        count=count,
        summations=tag
    )
    return resdata


# def partitions_dimension(data,tag,Liter):
#     '''
#     author: cst
#     统计每个标签的题目,多维中的一维,会多次循环调用
#     :param data:
#     :param tag:
#     :param Liter:
#     :return:
#     '''
#     tag = partitions(data,tag,Liter)
#     resdata = dict(
#         by=Liter[0],
#         summations=tag
#     )
#     return resdata


def get_literal(scope):
    '''
    author: cst
    英语科目每个复合类型都有特定的标签,其他科目只有固定几种标签
    update 17-11-16: 增加文理科科目标签分类信息
    :param scope:
    :return:
    '''
    if scope.get('koDiscipline') == 'english':
        comboFormat = scope.get('comboFormat')
        if comboFormat in ['simple-selection','fill-word-in-text','fill-word-in-sentence']:
            return [('QuestionEnglishComboObjectiveKind','objectiveOfCombo')]
        elif comboFormat in ['reading-comprehension','matching','cloze','read-write-task']:
            return [('QuestionMaterialKind','koMaterial'),('QuestionMaterialLengthDeg','materialLength')]  # todo   多种长度类型
        elif comboFormat in ['text-correction', 'sentence-correction']:
            return [('QuestionDifficultyKind','difficulty')]
        elif comboFormat in ['pattern-transformation', 'phrase-translation','sentence-translation','fill-word-in-sentence']:
            return
        else:
            raise ValueError
    elif scope.get('koDiscipline') in ["math","physics","chemistry","biology"]:
        return [
            ('QuestionResponseFormatKind','responseFormat'),
            ('QuestionDifficultyKind', 'difficulty'),
            ('QuestionSourceKind','koSource')
        ]
    elif scope.get('koDiscipline') in ["politics","geography","history"]:
        return [
            ('QuestionResponseFormatKindForArts', 'responseFormat'),
            ('QuestionDifficultyKind', 'difficulty'),
            ('QuestionSourceKind', 'koSource')
        ]
    else:
        raise ValueError

def statusMachine(signal,statusOfCheck):
    '''
    状态机 初始形态,未包含用户权限 todo
    :param signal:
    :param statusOfCheck:
    :return:
    '''
    status = ''
    if statusOfCheck == 'open' or statusOfCheck == None:
        if signal == 'pass':
            status = 'pass'
        elif signal == 'deny':
            status = 'deny'

    if statusOfCheck == 'pass' or statusOfCheck == 'deny':
        if signal == 'reset':
            status = 'open'
    return status


# def query_question(sonward,discipline=''):
#     '''
#     题目查询(只查题,获取某个指定节点下的题目,应该是单个节点)
#     :param sonward:
#     :param discipline:
#     :return:
#     '''
#     col_question = Question.coll()
#     if discipline == 'english':
#         volumes = [i.get('_id') for i in sonward if i.get('koLyro') == 'volume']
#         lookup = {"volume": {"$in":volumes},'koDiscipline':discipline}
#         questions = list(col_question.find(lookup))
#
#     else:  # 非英语学科
#         sections = [i.get('_id') for i in sonward if i.get('koLyro')=='section']
#         lookup = {"section": {"$in":sections},'koDiscipline':discipline}
#         questions = list(col_question.find(lookup))
#     return questions


def batch_stat_en(cat, question):
    '''
    将节下的题目统计信息合并整合为完整信息(英语)(英语题目和统计信息)
    :param cat: 章节列表
    :param stats: 节下的题目统计信息
    :param fullstat: 合并的统计信息
    :return:
    '''
    resp = {cat[0].get('name'): summations(question,cat[0])}
    resp_chapter = [i for i in question if "comboFormat" in i]
    resp_chapter.sort(key=itemgetter('comboFormat'))
    chapters = groupby(resp_chapter, itemgetter('comboFormat'))
    for key,groups in chapters: # 字段修改会导致查询出错，例如以前保存的数据作答形式单选为simpleselect,
        # 而数据库的枚举修改为simpleSelect这个就会出错，不catch错误，不然有数据未统计而未报错可能造成数据丢失，
        # 让其报错，清楚的知道有字段修改
        bot_son = getcombo_info(key)
        resp.update({key:summations(groups,bot_son)})
    return resp


def batch_stat(cat,stats,fullstat):
    '''
    将节下的题目统计信息合并整合为完整信息(非英语)具体的返回类型
    :param cat: 章节列表
    :param stats: 节下的题目统计信息
    :param fullstat: 合并的统计信息
    :return:
    '''
    son_list = cat.get('son')
    data = (stat for stat in stats if ObjectId(stat.get('scope').get('_id')) in son_list)
    count,state_1,state_2,state_3,state_4 = 0,0,0,0,0
    for stat in data:
        count += stat.get('count')
        state_1 += stat.get('summations')[0].get('count')
        state_2 += stat.get('summations')[1].get('count')
        state_3 += stat.get('summations')[2].get('count')
        state_4 += stat.get('summations')[3].get('count')
    resp = dict(
        count= count,
        scope= dict(
            _id=str(cat.get('_id')),
            name= cat.get('name'),
            title= cat.get('title')
        ),
        summations=[
            dict(
            criteria="state_1",
            count= state_1
        ),
            dict(
            criteria= "state_2",
            count= state_2
        ),
            dict(
            criterial= "state_3",
            count= state_3
        ),
            dict(
            criterial= "state_4",
            count= state_4
        )
        ]
    )
    fullstat.append(resp)


# def query_question_stat(sonward,botn,discipline=''):
#     '''
#     该id的统计信息(题目,节点统计信息)
#     :param sonward: 只统计自己
#     :param discipline: 科目类型
#     :return:
#     '''
#     col_question = Question.coll()
#     stats = []
#     if discipline == 'english':
#         volumes = [i.get('_id') for i in sonward if i.get('koLyro') == 'volume']
#         lookup = {"volume": {"$in":volumes},'koDiscipline':discipline}
#
#     else:  # 非英语学科
#         sections = [i.get('_id') for i in sonward if i.get('koLyro')=='section']
#         lookup = {"section": {"$in":sections},'koDiscipline':discipline}
#     questions = list(col_question.find(lookup))
#     data = summations(questions,botn)
#     stats.append(data)
#     return stats


# def query_questions_stat(sonward,discipline=''):
#     '''
#     所有id下的所有子节点的统计信息(题目,节点统计信息)
#     :param sonward: 所有的子节点包括自己
#     :param discipline: 科目类型
#     :return:
#     '''
#     col_question = Question.coll()
#     if discipline == 'english':
#         volumes = [i.get('_id') for i in sonward if i.get('koLyro') == 'volume']
#         lookup = {"volume": {"$in":volumes},'koDiscipline':discipline}
#         questions = list(col_question.find(lookup))
#         fullstat = batch_stat_en(sonward,questions)
#
#     else:  # 非英语学科
#         sections = [i.get('_id') for i in sonward if i.get('koLyro')=='section']
#         lookup = {"section": {"$in":sections},'koDiscipline':discipline}
#         questions = list(col_question.find(lookup))
#         ques = groupby(questions,itemgetter('section')) #  将题目按节分类
#         fullstat = []
#         stats = []
#         for k,v in ques:  # 节上的题目统计
#             for j in sonward:
#                 if j.get('_id') == k:
#                     data = summations(v,j)
#                     stats.append(data)
#                     continue
#         for cat in sonward:
#             if cat.get('koLyro') == 'chapter':
#                 batch_stat(cat,stats,fullstat)
#         for cat in sonward:
#             if cat.get('koLyro') == 'volume':
#                 batch_stat(cat,fullstat,fullstat)
#         fullstat.extend(stats)
#     return fullstat


def similar(name,id,limit=10):
    '''
    重题检测
    :param name:
    :return:
    '''
    '''重题算法'''
    col_question = Question.coll()
    data = list(col_question.find().limit(limit))
    data = dict(_items=data)
    resp =jsonify(json.loads(my_dump(data)))
    return resp


# def get_title_rows(json_ob):
#     title = []
#     row_num = 0
#     rows=[]
#     for key in json_ob:
#         title.append(key)
#         v = json_ob[key]
#         if len(v)>row_num:
#             row_num = len(v)
#         continue
#     for i in range(row_num):
#         row = []
#         for k in json_ob:
#             v = json_ob[k]
#             if i in v.keys():
#                 row.append(v[i])
#             else:
#                 row.append('')
#         rows.append(row)
#     return title, rows
#
#
# def json_to_csv(object_list):
#
#     # global json_ob, c_line
#     json_ob = {}
#     c_line = 0
#
#     def loop_data(o, k=''):
#         # global json_ob, c_line
#         if isinstance(o, dict):
#             for key, value in o.items():
#                 if (k == ''):
#                     loop_data(value, key)
#                 else:
#                     loop_data(value, k + '.' + key)
#         elif isinstance(o, list):
#             if not k in json_ob:
#                 json_ob[k] = {}
#             json_ob[k][c_line] = '|'.join(o)
#         else:
#             if not k in json_ob:
#                 json_ob[k] = {}
#             json_ob[k][c_line] = o
#
#     for ov in object_list :
#         loop_data(ov)
#         c_line += 1
#     title, rows = get_title_rows(json_ob)
#     content = [[str(i) for i in row] for row in rows]
#     head = ','.join(title)
#     data = '\n'.join([','.join(i) for i in content])
#     return head + '\n' + data

def json_to_csv(data):

    #"export to csv file"
    title = [
        "学科","角色类别","用户姓名","用户ID",
        "录题数量","打标数量","录题审核数量",
        "打标审核数量","题目所属章节目录"
    ]
    head = ','.join(title)

    ddl = []
    for line in data:
        ddll = [
            getcombo_info(
                line.get("user").get("discipline"),
                name='ExampaperDisciplineKind'
            ).get('title'),
            line.get("user").get("primaryTitle"),
            line.get("user").get("realname") or '',
            line.get("user").get("name"),
            str(line.get("typewritedCount")),
            str(line.get("taggedCount")),
            str(line.get("checkedTypeCount")),
            str(line.get("checkedTagCount"))]
        # if line.get("user").get("discipline") != "english":
        for lineinfo in line.get("partitions"):
            if "chapterCat" in lineinfo.get("by"):
                ddll.append("&".join([botn.get("botn").get("botntitle")
                    for botn in lineinfo.get("summations")]))
                continue
            if "volumeCat" in lineinfo.get("by"):
                ddll.append("||".join([botn.get("botn").get("botntitle")+" "+
                    getcombo_info(botn.get("botn").get("comboFormat")).get("title")
                    for botn in lineinfo.get("summations")]))
                continue
        ddl.append(ddll)
    lines = [",".join(line) for line in ddl]
    resp = head + "\n" + "\n".join(lines)
    return resp


def json_to_excel(data):

    #"export to csv file"
    title = [
        "学科","角色类别","用户姓名","用户ID",
        "录题数量","打标数量","录题审核数量",
        "打标审核数量","题目所属章节目录"
    ]
    head = ','.join(title)

    ddl = []
    for line in data:
        ddll = [
            getcombo_info(
                line.get("user").get("discipline"),
                name='ExampaperDisciplineKind'
            ).get('title'),
            line.get("user").get("primaryTitle"),
            line.get("user").get("realname") or '',
            line.get("user").get("name"),
            str(line.get("typewritedCount")),
            str(line.get("taggedCount")),
            str(line.get("checkedTypeCount")),
            str(line.get("checkedTagCount"))]
        # if line.get("user").get("discipline") != "english":
        if not line.get("partitions"):
            ddll.append("")
        for lineinfo in line.get("partitions"):
            if "chapterCat" in lineinfo.get("by"):
                ddll.append("&".join([botn.get("botn").get("botntitle")
                    for botn in lineinfo.get("summations")]))
                continue
            if "volumeCat" in lineinfo.get("by"):
                ddll.append("||".join([botn.get("botn").get("botntitle")+" "+
                    getcombo_info(botn.get("botn").get("comboFormat")).get("title")
                    for botn in lineinfo.get("summations")]))
                continue
        ddl.append(ddll)
    import pandas as pd
    pdData = pd.DataFrame(ddl)
    writer = pd.ExcelWriter('/tmp/output.xlsx')
    pdData.to_excel(writer,index=False,header=title)
    writer.save()


def ques_split(itemson,item):
    """
    含有子题的题目拆分
    :return:
    """

    if item.get('comboFormat') == 'matching':  # todo 信息匹配要自动打上标签
        if item.get('optionCount') == 7 and item.get('sonCount') == 6:
            pass
        elif item.get('optionCount') == 6 and item.get('sonCount') == 4:
            pass
        elif item.get('optionCount') == 5 and item.get('sonCount') == 4:
            pass
        else:
            pass

    if "son" not in item:
        item_id = item.pop("_id",None)
        origin_id = item_id or ObjectId()
        son_question = item.pop('fieldOfSon')
        soncount = item.pop('sonCount')
        # typewritedByFirstly = item.pop('typewritedByFirstly')#子题不保存录入人
        # typewritedAtFirstly = item.pop('typewritedAtFirstly')

        fieldK = [ k for k, v in son_question.items() if v]
        fieldV = [ v for k,v in son_question.items() if v] # 解答题有子题，但是没有子属性
        if fieldV:
            if son_question.get("contOfKey"): # 如果子属性有答案使用子属性的答案
                item.pop("contOfKey")
            son_extra = [dict(map(lambda x,y:[x,y[i]],fieldK,fieldV),
                              _id=ObjectId(), dad=origin_id, **item) for i in range(len(fieldV[0]))]
        else:
            son_extra = [dict({'_id': ObjectId(), 'dad': origin_id}, **item) for i in range(soncount)]
        son = [son['_id'] for son in son_extra]
        item.update(son=son,sonCount=soncount,fieldOfSon=son_question,
                    # typewritedByFirstly=typewritedByFirstly,
                    # typewritedAtFirstly=typewritedAtFirstly,
                    _id=origin_id)
        # if not item.get("contOfKey"):
        #     item.update(contOfKey=son_question.get("contOfKey")) #父题中加上答案
        # for i in son_extra:
        #     items.append(i)
        itemson.extend(son_extra)
    else:
        quests = []
        son = item.pop("son")
        typewritedAtFirstly = item.pop('typewritedAtFirstly')
        son_ids = []
        id = ObjectId()
        for fieldOfSon in son:
            son_id = ObjectId()
            fieldOfSon.update(item, dad=id, _id=son_id)
            son_ids.append(son_id)
            quests.append(fieldOfSon)
        item.update(_id=id, son=son_ids,typewritedAtFirstly=typewritedAtFirstly)
        itemson.extend(quests)
    return itemson


def add_subsource(quest):
    if "koSource" in quest:
        return getcombo_info(quest.get("koSource"),name="QuestionSourceKind")


def add_subsourceloca(quest):
    if "sourceLoca" in quest:
        return getcombo_info(quest.get("sourceLoca"),name="QuestionSourceLocaEnum")


def add_subresponseFormat(quest):
    if "responseFormat" in quest:
        return getcombo_info(quest.get("responseFormat"),name="QuestionResponseFormatKind")


def add_subcomboFormat(quest):
    if "comboFormat" in quest:
        return getcombo_info(quest.get("comboFormat"),name="EnglishQuestionComboFormatKind")


def add_derivedPath(quest):
    '''
    对于题目： 增加推导属性path
    英语题目： 科目 + 册 + 题目类型
    非英语题： 科目 + 册 + 章 + 节
    >>> add_derivedPath(quest)
    ["英语","高一","简单选择"]
    :param quest: 题目内容
    :return:
    '''
    col_bot = BOTNode.coll()
    discipline = quest.get("koDiscipline")

    if discipline == "english":
        combo = quest.get("comboFormat")
        volumeid = quest.get("volume")
        volume = col_bot.find_one(dict(_id=volumeid))
        path = [
            getcombo_info(discipline, name="QuestionDisciplineKind").get("title"),
            volume.get("title"),
            getcombo_info(combo, name="EnglishQuestionComboFormatKind").get("title")
        ]
    else:
        sectionid = quest.get("section")
        section = col_bot.find_one(dict(_id=sectionid))
        chapter = col_bot.find_one(dict(_id=section.get("dad")))
        volume = col_bot.find_one(dict(_id=chapter.get("dad")))
        path = [
            getcombo_info(discipline,name="QuestionDisciplineKind").get("title"),
            volume.get("title"),
            chapter.get("title"),
            section.get("title")
        ]
    return path