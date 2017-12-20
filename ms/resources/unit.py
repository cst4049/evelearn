import yaml
import json
from datetime import date, datetime

from bson import ObjectId,Decimal128
from flask import jsonify


class JSONEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, Decimal128):
            return int(str(o))
        return json.JSONEncoder.default(self, o)


def objectIds_convert_json(obj):
    return jsonify(json.loads(my_dump(obj),encoding="UTF-8"))


def my_dump(d):
    """
    将对象里的 所有ObjectId 都转化为 str
    来源: https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
    :param d:
    :return:
    """
    return JSONEncoder().encode(d)

def pre_insert(resource,req):
    pass


def burnavi(Q,R,M,Lyro,Lyri):
    pass


def allXxxLyro(resource, request, lookup):
    pass


def allXxxLyroTop(resource, request, lookup):
    pass


def allXxxLyroJust(resource, request, lookup):
    pass


def among(t,b):
    pass



class Chinese_Num_Map:
    @staticmethod
    def mapping_list():
        return yaml.load(open("./test/chinese_num_mapping.yaml"))

    @staticmethod
    def chinese_num_mapping(str_attr):
        mapping_list = Chinese_Num_Map.mapping_list()
        mapping_list = sorted(mapping_list,key= lambda item: -item["value"])
        for item in mapping_list:
            if item['name'] in str_attr:
                return item['value']
        return 0


