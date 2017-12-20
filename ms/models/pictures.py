import json

from bson import ObjectId
from flask import current_app as app


def post_POST_pictures(resource, request, lookup):
    if resource == 'pictures' and lookup._status_code == 201:
        resp = json.loads(lookup.response[0].decode('utf-8'))
        _id = resp.get("_id")
        picture = app.data.driver.db["pictures"]
        look_up = {'_id':ObjectId(_id)}
        respdata = picture.find_one(look_up)
        imgfileid = respdata.get("upload")
        prefix = app.config.get("SCHEME") + "://" + app.config.get("LDB_URI") if app.config.get("LDB_URI") else ''
        if len(imgfileid) == 1:
            url = prefix + "/" + app.config.get("MEDIA_ENDPOINT") +'/'+ str(imgfileid[0])
        else:
            url = [ prefix + "/" + app.config.get("LDB_URI") + app.config.get("MEDIA_ENDPOINT")+'/'+ str(imgid) for imgid in imgfileid ]
        resp['url'] = url
        resp['uploaded'] = 1
        resp['fileName'] = respdata.get("filename")
        resp = json.dumps(resp).encode('utf-8')
        lookup.response[0] = resp
        lookup.content_length = len(resp)