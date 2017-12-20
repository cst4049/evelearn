import re

from flask import g, json, request

from ms.models.Cache_Query_Optimize import Cache_Query_Optimize
from ms.resources.unit import objectIds_convert_json

"""
响应之后 根据flag 进行存储 即缓存
"""
def set_cache(resp):
    if g.get("cache_flag") == True and resp._status_code == 200:
        result_cache = json.loads(resp.data)
        _id = Cache_Query_Optimize.coll().insert({"name":g.cache_path,"value":result_cache})
    pass
    return resp



def cache_interceptor():
    path = re.search('bok-nodes/[a-f0-9A-F]{24}/son[warden]{3,4}', request.base_url)
    if path != None:
        #说明符合条件
        query_path = get_query_path(request.full_path)
        #返回的是缓存的值,而不是数据中的对象
        cache_result = Cache_Query_Optimize.coll().find_one({"name":query_path})
        if cache_result != None:
            return objectIds_convert_json(cache_result['value']),200
        g.cache_flag = True
        g.cache_path = query_path


def get_query_path(req_full_path):
    token_url = re.search('&token=\w+\.\w+\.[\w-]+', req_full_path).group()
    return req_full_path.replace(token_url, "")
