from bson import ObjectId
from flask import abort
from flask import current_app as app
from  werkzeug.datastructures import ImmutableMultiDict

from ms.hooks.taginfo import similar
from ms.models.Question import Question
from ms.models.ROLE import Role


def pre_get_questions(request,lookup):
    args = request.args  # 请求参数
    if args.get('similar_to'):
        similar_id = args.get('similar_to')
        if args.get('limit'):
            limit = int(args.get('limit')) or app.config.get("SIMILAR_COUNT")
        resp = similar(request.view_args['quesBank'], similar_id, limit)
        abort(resp)
    lookup = Question.parserargs(request, lookup)
    if lookup:
        if "botn" in lookup:
            lookup.pop("botn")
        arginfo = {}
        if args.get("max_results"):
            arginfo.update(max_results=args.get("max_results"))
        if args.get("page"):
            arginfo.update(page=args.get("page"))
        if args.get("projection"):
            arginfo.update(page=args.get("projection"))
        if args.get("sort"):
            arginfo.update(page=args.get("sort"))
        request.args = arginfo
        request.args = ImmutableMultiDict(request.args)
    lookup = Role.authcheck("Get",lookup)
    # if g.user.get("primaryRole") == "xk_cb_typewritist": #todo 合并权限
    #     lookup.update(typewritedByFirstly=g.user.get("_id"))


def pre_post_questions(request):
    req = request.json
    if isinstance(req,list):
        for ques in req:
            Role.authcheck("Type", req)

    elif isinstance(req,dict):
        Role.authcheck("Type",req)
        # if g.user.get("primaryRole") == "xk_cb_typewritist": #todo 合并权限
        #     if req.get("koDiscipline") != g.user.get("primaryDiscipline"):
        #         abort(403,description="not allow to add question")


def pre_patch_questions(request,lookup):
    lookup["_id"] = ObjectId(lookup.get("_id"))
    req = Question.coll().find_one(lookup)
    Role.authcheck("Type",req)
    # if g.user.get("primaryRole") == "xk_cb_typewritist": #todo 合并权限
    #     if req.get("koDiscipline") != g.user.get("primaryDiscipline"):
    #         abort(403,description="not allow to add question")


def pre_delete_questions(request,lookup):
    lookup["_id"] = ObjectId(lookup.get("_id"))
    req = Question.coll().find_one(lookup)
    Role.authcheck("Delete", req)
    # if g.user.get("primaryRole") == "xk_cb_typewritist": #todo 合并权限
    #     if req.get("koDiscipline") != g.user.get("primaryDiscipline"):
    #         abort(403,description="not allow to add question")

