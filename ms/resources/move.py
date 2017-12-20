from bson import ObjectId
from flask import jsonify
from flask import request

from ms.hooks.taginfo import getczj_info, getcombo_info
from ms.models.Question import Question


def moveto(para):
    question,name,d = para
    botninfo,comboinfo='',''
    id = d.get('_id')
    if 'botn' in d:
        botn = d.get('botn')
        botninfo = getczj_info(botn)
    if 'comboFormat' in d:
        combo = d.get('comboFormat')
        comboinfo = getcombo_info(combo)

    lookup = {'quesBank':name,'_id':ObjectId(id)}
    data = question.find_one(lookup)

    res = {
        '_id':id
    }

    if not data and not botninfo and not comboinfo:
        res.update(info = 'parame may not correct')
        return res

    if botninfo and not comboinfo:
        update = {'$set':{botninfo.get('koLyro'):ObjectId(botn)}}
        upinfo = question.update_one(lookup,update)
        status = 'move success' if upinfo.raw_result.get('ok') else 'move fail'
    elif comboinfo and not botninfo:
        update = {'$set': {'comboFormat': combo}}
        upinfo = question.update_one(lookup,update)
        status = 'move success' if upinfo.raw_result.get('ok') else 'move fail'
    elif comboinfo and botninfo:
        update = {'$set': {'comboFormat': combo,botninfo.get('koLyro'):ObjectId(botn)}}
        upinfo = question.update_one(lookup,update)
        status = 'move success' if upinfo.raw_result.get('ok') else 'move fail'
    else:
        status = 'please check your parameter'
    res.update(info = status)
    return res


def move(name):
    '''批量移动'''
    question = Question.coll()
    args = request.json
    if isinstance(args,list):
        para = [(question,name,d) for d in args]
        data = list(map(moveto, para))
    if isinstance(args,dict):
        para = (question,name,args)
        data = moveto(para)
    resp = jsonify(data)
    return resp