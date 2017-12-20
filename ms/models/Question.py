import datetime
import json

from bson import ObjectId
from flask import abort
from flask import current_app as app
from flask import g

from ms.models.BOT import BOTNode
from ms.models.Users import Users
from ms.resources.burtree_node import recursion_structuring


class Question:

    # 题目相关
    @staticmethod
    def coll():
        col = app.data.driver.db['questions']
        return col

    @staticmethod
    def get_discipline():
        discipline = ''
        return discipline

    @staticmethod
    def get_checkStatus():
        checkStatus = ''
        return checkStatus

    @staticmethod
    def istaged(id):
        if isinstance(id,str):
            id = ObjectId(id)
        lookup = {"_id":id}
        quest = Question.coll(lookup)
        if quest.get("son"):
            lookup = {"_id":{"$in":quest.get("son")}}
            sque_tag = [sques for sques in list(Question.coll().find(lookup)) if
                        sques.get("boknCat") or sques.get("difficulty")]
            if sque_tag:
                return True
            return False
        else:
            if quest.get("boknCat") or quest.get("difficulty"):
                return True
            return False
    pass

    # 将这个函数替换为下面更为通用的函数
    # @staticmethod
    # def parsearg(request,lookup,botn=None):
    #     '''
    #     参数解析，英语非英语
    #     :param request:
    #     :param lookup:
    #     :param botn:
    #     :return:
    #     '''
    #     scope = json.loads(request.args.get('scope'))
    #     if scope:  # scope 控制范围,如果没有这个参数默认查询name题库下所有
    #         lookup.update(scope)
    #         lyro = []
    #         if 'botn' in scope:
    #             botnid = scope.get('botn')
    #             recursion_structuring(botnid, lyro, botn)
    #             if scope.get('koDiscipline') == 'english':
    #                 vid = [i.get('_id') for i in lyro if i.get('koLyro') == 'volume']
    #                 lookup.update({"$or": [{"volume": {"$in": vid}}]})
    #             else:
    #                 sid = [i.get('_id') for i in lyro if i.get('koLyro') == 'section']
    #                 lookup.update({"$or": [{"section": {"$in": sid}}]})
    #             lookup.pop('botn')
    #     return lookup

    @staticmethod
    def parserargs(request, lookup):
        '''
        参数解析，英语非英语test
        :param request:
        :param lookup:
        :param botn:
        :return:
        '''
        payload = request.args
        where = json.loads(payload.get("where")) if payload.get("where") else None \
            or json.loads(payload.get("scope")) if payload.get("scope") else None
        states = payload.get("state_in")
        if where:
            koDiscipline = where.get("koDiscipline")
            if "botn" in where or "sonern-of" in payload: # botn 可能是英语ID，也可能是非英语ID;可能是册也可能是章ID
                if payload.get("sonern-of"):
                    where["botn"] = payload.get("sonern-of")
                botnid = where.get("botn")
                botns = []  # botn是section或者volume
                recursion_structuring(botnid,botns,BOTNode.coll()) #所有子节点(含自己)
                if not botns:
                    abort(404,description="this botn is not found") # 这个节点数据库中没有
                if koDiscipline == "english":
                    volid = [botn.get("_id") for botn in botns
                             if botn.get("koLyro") == "volume"]
                    lookup.update({"volume": {"$in": volid}})
                else:
                    secid = [botn.get("_id") for botn in botns
                             if botn.get("koLyro") == "section"]
                    lookup.update({"section": {"$in": secid}})
            elif where.get("section"): #数据库查询Id需要转换为objectid
                where["section"] = ObjectId(where.get("section"))
            elif where.get("volume"):
                where["volume"] = ObjectId(where.get("volume"))
            lookup.update(where)
        if states:
            sta = [int(state) for state in states.split(',')]
            lookup.update(state={"$in":sta})
        #增加权限？todo
        return lookup

    @staticmethod
    def on_signal(ctx, signal):
        """

        :param ctx: 作为状态机的上下文环境对象，这里也就是question，或者question的id
        :param signal: 作为触发状态机变化的信号（指实例）
        :return:
        """

        if not ( signal in ['created', 'check-typewrite-pass', 'check-typewrite-reset',
                            'tagged', 'check-tag-pass', 'check-tag-reset'] ):
            raise "err"

        if isinstance(ctx, (str,ObjectId)) and ObjectId.is_valid(ctx):
            q = Question.coll().find_one(ObjectId(ctx))
        elif isinstance(ctx, dict):
            q = ctx
        elif ctx is None:
            q = {}
        else:
            raise "err"

        srcState = q.get("state") if q else None
        tgtState = None

        isConsumed = False;

        if srcState == None:
            if signal == "created" :
                tgtState = 1
                isConsumed = False if srcState == tgtState else True

        if srcState == 1 and signal != 'created': # 在录或录毕 状态
            if signal == "check-typewrite-pass" :
                tgtState = 2
                isConsumed = False if srcState == tgtState else True

        elif srcState == 2:
            if signal == "check-typewrite-reset":
                tgtState = 1
                isConsumed = False if srcState == tgtState else True
            elif signal == "tagged":
                tgtState = 3
                isConsumed = False if srcState == tgtState else True
            else:
                isConsumed = False

        elif srcState == 3:
            if signal == "check-typewrite-reset":
                tgtState = 1
                isConsumed = False if srcState == tgtState else True
            elif signal == "check-tag-pass":
                tgtState = 4
                isConsumed = False if srcState == tgtState else True
            else:
                isConsumed = False

        elif srcState == 4:
            if signal == "check-tag-reset":
                tgtState = 3
                isConsumed = False if srcState == tgtState else True
            else:
                isConsumed = False


        if (isConsumed):
            return tgtState
        else:
            return "ignored"


    # def do_statis(iterlist):
    #     '''
    #     分组,按照指定的字段分组列表
    #     :return:
    #     '''
    #     d = {}
    #     for k,v in iterlist:
    #         l = []
    #         for val in v:
    #            l.append(val)
    #         d.update({k:l})
    #     return d
    #
    #
    # def get_userlist(entered,taged,checked):
    #     '''
    #     获取三种信息的所有用户,去除重复
    #     :param taged:
    #     :param checked:
    #     :return:
    #     '''
    #     alist = []
    #     _no = [alist.extend(list(i)) for i in [entered,taged,checked]]
    #     ulist = set(alist)
    #     userL = []
    #     for uid in ulist:
    #         if uid in entered:
    #             if entered.get(uid):
    #                 user = entered.get(uid)[0].get('enteredman')[0]
    #         elif uid in taged:
    #             if taged.get(uid):
    #                 user = taged.get(uid)[0].get('tagedman')[0]
    #         elif uid in checked:
    #             if checked.get(uid):
    #                 user = checked.get(uid)[0].get('checkedman')[0]
    #         else:
    #             raise ValueError
    #         userL.append(user)
    #     return userL
    #
    # @staticmethod
    # def get_stat(question, lookup, discipline, role, start, to):
    #     '''
    #     获取状态信息
    #     :param question:
    #     :param lookup:
    #     :param discipline:
    #     :param role:
    #     :param start:
    #     :param to:
    #     :return:
    #     '''
    #     #db.question.aggregate({"$match": {"_id": ObjectId("59e6bb970b4b4b255db46a69")}}, {
    #     #    "$lookup": {"localField": "taggedByFirstly", "from": "users", "foreignField": "_id", "as": "taggedByFirstly"}})
    #     if discipline:
    #         lookup.update(koDiscipline=discipline)
    #     #if role:  # 内嵌文档的查询
    #     #    lookup.update(role=role)
    #     if start and not to:
    #         start = datetime.datetime.strptime(start,'%Y-%m-%d')
    #         lookup.update({'_created':{'$gte':start}})
    #     if to and not start:
    #         to = datetime.datetime.strptime(to, '%Y-%m-%d')
    #         lookup.update({'_created':{'$lte':to}})
    #     if start and to:
    #         start = datetime.datetime.strptime(start, '%Y-%m-%d')
    #         to = datetime.datetime.strptime(to, '%Y-%m-%d')
    #         lookup.update({'$and': [{'_created':{'$gte':start}},
    #                                 {'_created':{'$lte':to}}]})
    #
    #     project = {'_created':0,"_id":0,"_updated":0,"_version":0,
    #                'enteredman._created':0,"enteredman._updated":0,
    #                "enteredman._version":0,"enteredman.passwd":0,
    #                'tagedman._created':0,"tagedman._updated":0,
    #                "tagedman._version":0,"tagedman.passwd":0,
    #                'checkedman._created':0,"checkedman._updated":0,
    #                "checkedman._version":0,"checkedman.passwd":0
    #                }
    #
    #     _lookup = [
    #         {"$match": lookup},
    #         {"$lookup": {"localField": "typewritedByFirstly", "from": "users",
    #                      "foreignField": "_id", "as": "enteredman"}},
    #         {"$lookup": {"localField": "taggedByFirstly", "from": "users",
    #                      "foreignField": "_id", "as": "tagedman"}},
    #         {"$lookup": {"localField": "checkedByFirstly", "from": "users",
    #                      "foreignField": "_id", "as": "checkedman"}},
    #         # {"$match":{"$or":[{"enteredman.primaryRole":role},
    #         # {"tagedman.primaryRole":role},{"checkedman.primaryRole":role}]}
    #         # if role else {}},
    #         {"$project": project}
    #     ]
    #
    #     data = list(question.aggregate(_lookup))  #获取所有的数据
    #
    #     data_entered = (i for i in data if 'typewritedByFirstly' in i)
    #     entered = groupby(data_entered,itemgetter('typewritedByFirstly'))
    #
    #     data_taged = (i for i in data if 'taggedByFirstly' in i)
    #     taged = groupby(data_taged,itemgetter('taggedByFirstly'))
    #
    #     data_checked = (i for i in data if 'checkedByFirstly' in i)
    #     checked = groupby(data_checked,itemgetter('checkedByFirstly'))
    #
    #     info_entered = Question.do_statis(entered)
    #     info_taged = Question.do_statis(taged)
    #     info_checked =Question.do_statis(checked)
    #
    #     userlist = Question.get_userlist(info_entered,info_taged,info_checked)
    #     static = []
    #     for user in userlist:
    #         if not role or user.get('primaryRole') == role and not discipline or user.get('primaryDiscipline') == discipline:
    #             user_for_enter = [ques for ques in (i for i in data if 'typewritedByFirstly' in i)
    #                               if ques.get('typewritedByFirstly') == user.get('_id')]
    #             user_for_tag = [ques for ques in (i for i in data if 'taggedByFirstly' in i)
    #                             if ques.get('taggedByFirstly') == user.get('_id')]
    #             user_for_check = [ques for ques in (i for i in data if 'checkedByFirstly' in i)
    #                               if ques.get('checkedByFirstly') == user.get('_id')]
    #             # if user_for_enter: # 时间排序
    #             #     start_time = min(user_for_enter,key=lambda s:s['_created'])
    #             #     end_time = max(user_for_enter,key=lambda s:s['_created'])
    #             if user.get('primaryDiscipline') == 'english':
    #                 comboFormat = set([(i.get('comboFormat'),i.get('volume')) for i in user_for_enter]) | \
    #                               set([(i.get('comboFormat'),i.get('volume')) for i in user_for_tag]) | \
    #                               set([(i.get('comboFormat'),i.get('volume')) for i in user_for_check])
    #                 dist = list(comboFormat)
    #                 distribution = {'partition':dist.remove(None) if None in dist else dist}
    #
    #             else:
    #                 section = set([i.get('section') for i in user_for_enter]) | \
    #                               set([i.get('section') for i in user_for_tag]) | \
    #                               set([i.get('section') for i in user_for_check])
    #                 section = list(section)
    #                 if section:
    #                     botn = BOTNode.coll()
    #                     botn_chapter = list(botn.find({'_id':{'$in':section}},{'_id':0}))
    #                     chapter = set(i.get('dad') for i in botn_chapter)
    #                     dist = list(chapter)
    #                     distribution = {'chapter': dist.remove(None) if None in dist else dist}
    #                     distribution.update({"section":section.remove(None) if None in section else section})
    #                 else:
    #                     dist = {}
    #             static.append({
    #                 "user": user,
    #                 "entered": len(user_for_enter),
    #                 "taged": len(user_for_tag),
    #                 "checked": len(user_for_check),
    #                 "distribution": distribution
    #             })
    #
    #     return static

    @staticmethod
    def jobargs(request,lookup):
        '''
        获取资源库统计状态信息
        :param question:
        :param lookup:
        :param discipline:
        :param role:
        :param start:
        :param to:
        :return:
        '''
        # 保存请求信息
        args = request.args
        discipline = args.get('discipline')
        role = args.get('role')
        start = args.get('from')
        to = args.get('to')
        alt = args.get('alt')

        scope = dict(
            period_b=start,
            period_e=to,
            discipline=discipline,
            role=role,
            alt=alt
        )
        if discipline:
            lookup.update(koDiscipline=discipline)
        if start and not to:
            start = datetime.datetime.strptime(start,'%Y-%m-%d')
            lookup.update(_created={'$gte':start})
        if to and not start:
            to = datetime.datetime.strptime(to, '%Y-%m-%d')
            lookup.update(_created={'$lte':to})
        if start and to:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
            to = datetime.datetime.strptime(to, '%Y-%m-%d')
            lookup.update({'$and': [{'_created':{'$gte':start}},
                                    {'_created':{'$lte':to}}]})

        project = {'_created':0,"_updated":0,"_version":0,
                   'typewritedBy._created':0,"typewritedBy._updated":0,
                   "typewritedBy._version":0,"typewritedBy.passwd":0,
                   'taggedBy._created':0,"taggedBy._updated":0,
                   "taggedBy._version":0,"taggedBy.passwd":0,
                   'checkedTypeBy._created':0,"checkedTypeBy._updated":0,
                   "checkedTypeBy._version":0,"checkedTypeBy.passwd":0,
                   'checkedTagBy._created': 0, "checkedTagBy._updated": 0,
                   "checkedTagBy._version": 0, "checkedTagBy.passwd": 0
                   }

        _lookup = [
            {"$match": lookup},
            {"$lookup": {"localField": "typewritedByFirstly", "from": "users",
                         "foreignField": "_id", "as": "typewritedBy"}},
            {"$lookup": {"localField": "taggedByFirstly", "from": "users",
                         "foreignField": "_id", "as": "taggedBy"}},
            {"$lookup": {"localField": "checkedTypeByFirstly", "from": "users",
                         "foreignField": "_id", "as": "checkedTypeBy"}},
            {"$lookup": {"localField": "checkedTagByFirstly", "from": "users",
                         "foreignField": "_id", "as": "checkedTagBy"}},
            # {"$match":{"$or":[{"enteredman.primaryRole":role},
            # {"tagedman.primaryRole":role},{"checkedman.primaryRole":role}]}
            # if role else {}},
            {"$project": project}
        ]
        return scope,_lookup

    @staticmethod
    def jobstat(lookup,scope):
        dataquestions = list(Question.coll().aggregate(lookup))
        #获取所有的用户(录过题，打过标，审核过的用户，未审核，未打标，未录题的不会显示)
        # userlist = [quest.get("typewritedBy")[0] for quest in dataquestions if quest.get("typewritedBy")] + \
        #     [quest.get("taggedBy")[0] for quest in dataquestions if quest.get("taggedBy")] + \
        #     [quest.get("checkedBy")[0] for quest in dataquestions if quest.get("checkedBy")]
        # userset = []
        # _userset = [userset.append(user) for user in userlist if user not in userset]
        jobstat = []
        userfilter = dict(_deleted=False)
        userproject = dict(
            _created=0,
            _updated=0,
            _version=0,
            passwd=0
        )

        userset = list(Users.coll().find(userfilter,userproject))
        scope["discipline"] = g.user.get("primaryDiscipline") if g.user.get("primaryRole") == "xk_subadmin" else \
            scope["discipline"]
        # if not scope.get("role",None):
        #     userset = [ u for u in userset if u.get('primaryRole') == scope.get("role") ]
        # if scope.get("discipline",None) != None:
        #     userset = [ u for u in userset if u.get('primaryDiscipline') == scope.get("discipline") ]

        for user in userset:
            if (not scope.get("role") or \
                user.get('primaryRole') == scope.get("role")) and \
                (not scope.get("discipline") or \
                user.get('primaryDiscipline') == scope.get("discipline")):
                _dataquestions=''
                if not scope.get("discipline"):  # 没有指定科目时,会根据用户的自身科目属性获取该科目的题目
                    _dataquestions = [q for q in dataquestions if user.get("primaryDiscipline") == q.get("koDiscipline")]
                questforuserset = []
                questforuser = [quest for quest in _dataquestions or dataquestions
                     if quest.get("typewritedBy") and quest.get("typewritedBy")[0] == user] + \
                    [quest for quest in _dataquestions or dataquestions
                     if quest.get("taggedBy") and quest.get("taggedBy")[0] == user] + \
                    [quest for quest in _dataquestions or dataquestions
                     if quest.get("checkedTypeBy") and quest.get("checkedTypeBy")[0] == user ]+ \
                    [quest for quest in _dataquestions or dataquestions
                     if quest.get("checkedTagBy") and quest.get("checkedTagBy")[0] == user ]
                _questforuserset = [questforuserset.append(quest) for quest in questforuser
                                    if quest not in questforuserset]
                #题目的录入打标审核所在的册、章、节信息
                scoped = list(set(quest.get("section") for quest in questforuserset if quest.get("section")))

                scoped_chapter = list(set(BOTNode.coll().find_one({"_id":id}).get("dad") for id in scoped if BOTNode.coll().find_one({"_id":id})))
                # if user.get("name")=="lty_sx_001":
                #     print("aa")
                _scoped_chapter = (dict(botn=BOTNode.coll().find_one({"_id": id}).get("_id"),
                                        volume=BOTNode.coll().find_one({"_id": id}).get("dad"),
                                       botntitle=BOTNode.coll().find_one({"_id": id}).get("title")
                                       ) for id in scoped_chapter if BOTNode.coll().find_one({"_id": id}))
                scoped_chapter = []
                _scoped_chapter = [scoped_chapter.append(chapter) for chapter in _scoped_chapter
                                    if chapter not in scoped_chapter]

                if None in scoped_chapter:
                    scoped_chapter.pop(None)
                _volume = [dict(id,**BOTNode.coll().find_one({"_id": id.get("volume")}, {"title": 1, "discipline": 1,"_id":0})) for id in scoped_chapter
                           if BOTNode.coll().find_one({"_id": id.get("volume")})]

                scoped_en = []
                _scoped_en = ((dict(botn=quest.get("volume"),comboFormat=quest.get("comboFormat"))
                               for quest in questforuserset if quest.get("volume"))) #generate 获取英语分布
                _scoped_en = [scoped_en.append(volcomb) for volcomb in _scoped_en
                                    if volcomb not in scoped_en]
                scope_en1 = [volume.update(botntitle=BOTNode.coll().find_one({"_id":volume.get("botn")}).get("title")) for volume in scoped_en if BOTNode.coll().find_one({"_id":volume.get("botn")})]



                part = []
                # if scoped: # 增加section分区
                #     part.append((dict(sectionCat=1),scoped))
                if scoped_chapter: # 以章分区
                    part.append((dict(chapterCat=1),_volume))
                if scoped_en:
                    part.append((dict(
                        volumeCat=1,
                        comboFormat=1
                    ),scoped_en))

                summations = dict(
                    criteria = dict(
                        participater=user.get("name")
                    ),
                    user=dict(
                        discipline=user.get("primaryDiscipline"),
                        primaryRole=user.get("primaryRole"),
                        primaryTitle=user.get("description"),
                        name=user.get("name"),
                        id=user.get("_id"),
                        realname=user.get("realname")
                    ),
                    typewritedCount=len([i for i in questforuserset if i.get("typewritedByFirstly") == user.get("_id")]),
                    taggedCount=len([i for i in questforuserset if i.get("taggedByFirstly") == user.get("_id")]),
                    checkedTypeCount=len([i for i in questforuserset if i.get("checkedTypeByFirstly") == user.get("_id")]),
                    checkedTagCount=len([i for i in questforuserset if i.get("checkedTagByFirstly") == user.get("_id")]),
                    count=len(questforuserset),
                    scoped=[quest.get("_id") for quest in questforuserset],
                    partitions=[dict(by=by,summations=[{"botn":i} for i in summation]) \
                                for by,summation in part if by and summation]
                )
                jobstat.append(summations)
        if not jobstat:
            return jobstat,0
        return jobstat,len(questforuserset)