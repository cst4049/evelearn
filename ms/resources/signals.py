from flask import g
from flask import request

from ms.hooks.taginfo import *
from ms.models.ROLE import Role


# def aa(id):
#     '''
#     查找题目
#     :param id:
#     :return:
#     '''
#     sonward = ques_status(id)
#     questions = query_question(sonward)
#     resp = jsonify({'_items':json.loads(my_dump(questions))})
#     return  resp


def convert_signal(para):
    '''
    查找状态信息,修改状态信息
    :param para:
    :return:
    '''
    checkmap = {
        "typewrite": "statusTypeOfCheck",
        "tag": "statusTagOfCheck"
    }
    question,name,id,siginfo = para
    lookup = {"quesBank": name, "_id": id}
    quest = question.find_one(lookup)
    checkT,signal = siginfo.split("-")[1:]
    if quest:
        code = Role.authcheck(checkT+"Check",quest)
        if code == 403:
            res = dict(
                id=str(id),
                status='check is forbiden'
            )
            return res
        statusOfCheck = quest.get(checkmap[checkT])
        if checkT == "typewrite":
            update = dict()
            if not quest.get("checkedTypeAtFirstly"):
                update.update(dict(checkedTypeAtFirstly=datetime.now(),
                                   checkedTypeByFirstly=g.user.get("_id") # token获取
                                   ))
            update.update(checkedTypeAtLastly=datetime.now())
            status = statusMachine(signal, statusOfCheck)
            if status:  # 当状态需要改变status有值,否则该条请求可以忽略
                update.update(statusTypeOfCheck=status)
                state = Question.on_signal(id,siginfo)
                if state in [1,2,3,4]:
                    update.update(state=state)
                info = question.update_one(lookup, {"$set": update})
                if info.raw_result.get('ok'):
                    res = {'status': status, "_id": str(id)}
                else:
                    res = {'status': statusOfCheck, 'update': 'defeat', "_id": str(id)}
            else:
                res = {'status': 'ignored', "_id": str(id)}
        else:
            update = dict()
            if not quest.get("checkedTagAtFirstly"):
                update.update(dict(checkedTagAtFirstly=datetime.now(),
                                   checkedTagByFirstly=g.user.get("_id") # token获取
                                   ))
            update.update(checkedTagAtLastly=datetime.now())
            status = statusMachine(signal, statusOfCheck)
            if status:  # 当状态需要改变status有值,否则该条请求可以忽略
                update.update(statusTagOfCheck=status)
                state = Question.on_signal(id, siginfo)
                if state in [1,2,3,4]:
                    update.update(state=state)
                info = question.update_one(lookup, {"$set": update})
                if info.raw_result.get('ok'):
                    res = {'status': status, "_id": str(id)}
                else:
                    res = {'status': statusOfCheck, 'update': 'defeat', "_id": str(id)}
            else:
                res = {'status': 'ignored', "_id": str(id)}
    else:
        res = {"error": "question not found"}
    return res


def signal(name,id,signal):
    '''
    signal信号
    :param name:
    :param id:
    :param signal:
    :return:
    '''
    question = Question.coll()
    id = ((question,name,ObjectId(i),signal) for i in id.split(','))
    data = list(map(convert_signal,id))
    resp = jsonify(dict(_items=data))
    return resp


def signaltest(name,id):
    '''
    signal信号
    :param name:
    :param id:
    :param signal:
    :return:
    '''
    signal = request.headers.environ.get("HTTP_X_SPUR_SIGNAL")
    status = Question.on_signal(ObjectId(id), signal)
    return status