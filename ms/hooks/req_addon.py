from flask import abort
from flask import current_app as app
from  werkzeug.datastructures import ImmutableMultiDict

from .taginfo import *
from flask import abort


def pre_GET(resource, request, lookup):
    # if resource == 'questions':
    #     args = request.args # 请求参数
    #     if args.get('similar_to'):
    #         similar_id = args.get('similar_to')
    #         if args.get('limit'):
    #             limit = int(args.get('limit')) or app.config.get("SIMILAR_COUNT")
    #         resp = similar(request.view_args['quesBank'], similar_id, limit)
    #         abort(resp)
    #     lookup = Question.parserargs(request,lookup)
    #     if lookup:
    #         if "botn" in lookup:
    #             lookup.pop("botn")
    #         arginfo = {}
    #         if args.get("max_results"):
    #             arginfo.update(max_results=args.get("max_results"))
    #         if args.get("page"):
    #             arginfo.update(page=args.get("page"))
    #         request.args = arginfo
    #         request.args = ImmutableMultiDict(request.args)
    pass



def pre_PATCH(resource, request, lookup):
    pass


def pre_PUT(resource, request, lookup):
    pass

def pre_POST(resource, request):
    # if resource == 'tag':
    #     question = app.data.driver.db['question']
    #     lookup = ObjectId(request.view_args.get('_id'))
    #     aa = question.update_one({'_id':lookup},{'$set':{"contOfQuery":"eeeeeeeeeeeaaaabbbb"}})
    #     exit() todo
    # if resource == "questions":
    #     req = request.json
    #     if req.get("koDiscipline") == "english" and "section" in req:
    #         request.json.pop("section")
    # request.data = str(request.json).encode("utf-8")
    pass


def pre_DELETE(resource, request, lookup):
    pass


def post_GET(resource, request, lookup):
    pass

    return
    # if resource == "botn-sonern" and lookup._status_code == 200:
    #     #根据 id去查对应  botn
    #     #pop出 son  , for循环 查DB  查询条件  dad= 这个ID
    #     base_url_str = request.base_url
    #     _id =  re.search('[a-f0-9A-F]{24}',base_url_str).group()
    #     botnCollection = app.data.driver.db["botn"]
    #     sons = botnCollection.find({'dad':ObjectId(_id)})
    #     list =[]
    #     for son_item in sons:
    #         list.append(json.loads(my_dump(son_item)))
    #
    #
    #     #组装返回结果
    #     resp = json.loads(lookup.response[0].decode('utf-8'))
    #     resp.update(_items=list)
    #     resp['_meta']['total'] = len(list)
    #
    #
    #     lookup.response[0] = json.dumps(resp).encode('utf-8')
    #     lookup.content_length = len(json.dumps(resp).encode('utf-8'))
    #
    # if resource == 'botn-sonward' and lookup._status_code == 200:
    #     """
    #     外层通上, 内层获取 list使用递归
    #     """
    #     base_url_str = request.base_url
    #     _id = re.search('[a-f0-9A-F]{24}',base_url_str).group()
    #
    #     botnCollection = app.data.driver.db['botn']
    #     list=[]
    #     recursion_structuring(_id,list,botnCollection )
    #     list_new=[]
    #     for i in list:
    #         dict_item = {}
    #         for k ,v in i.items():
    #             dict_item[k]=v.__str__()
    #         list_new.append(dict_item)
    #     list= list_new
    #
    #     resp = json.loads(lookup.response[0].decode('utf-8'))
    #     resp.update(_items=list)
    #     resp['_meta']['total'] = len(list)
    #     lookup.response[0] = json.dumps(resp).encode('utf-8')
    #     lookup.content_length = len(json.dumps(resp).encode('utf-8'))
    #     pass



def post_PATCH(resource, request, lookup):
    pass


def post_PUT(resource, request, lookup):
    pass


def post_DELETE(resource, request, lookup):

    pass
    # if resource == 'questionbank' and lookup._status_code == 204:
    #     _id = request.get("view_args").get("_id")
    #     question = app.data.driver.db["question"]
    #     picture = app.data.driver.db["picture"]
    #     look_up = {'QuestionBank':ObjectId(_id)}
    #     resp = question.update(look_up,{"$set":{"_deleted":True}},False,True)
    #     resp = picture.update(look_up, {"$set": {"_deleted": True}}, False, True)
    #
    # if resource == 'question' and lookup._status_code == 204:
    #     _id = request.get("view_args").get("Question")
    #     picture = app.data.driver.db["picture"]
    #     look_up = {'Question':ObjectId(_id)}
    #     respdata = question.update(look_up,{"$set":{"_deleted":True}},False,True)


def recursion_structuring_copy(_id ,list,mongoDB_collection):
    '''
    复制上面的recursion_structuring_copy,缺一个返回参数koLyro,后期review在合并 todo
    :param _id:
    :param list:
    :param mongoDB_collection:
    :return:
    '''
    node = mongoDB_collection.find_one({'_id':ObjectId(_id)},{'name':1,'_id':1,'dad':1,'son':1,'title':1,'koLyro':1})
    if node:
        if 'son' in node.keys():
            for son_item in node['son']:
                recursion_structuring_copy(son_item, list, mongoDB_collection)
        list.append(node)

def ques_status(id):
    mongoDB_collection = BOTNode.coll()
    list = []
    recursion_structuring_copy(id,list,mongoDB_collection)
    return list
