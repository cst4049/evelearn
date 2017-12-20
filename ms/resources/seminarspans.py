import arrow
from bson import ObjectId

from ms.models.Seminar import Seminar
from ms.models.SeminarSpans import SeminarSpans


def post_PATCH_seminarspans_insert_activeTime(request, payload):
    seminar_id = request.json.get("active")
    #model.Seminar.setActiveTime( seminar_id)
    if seminar_id != None:
        seminar_ins = Seminar.coll().find_one({"_id":ObjectId(seminar_id)})
        if seminar_ins != None:
            SeminarSpans.coll_seminars().update({
             "_id": seminar_ins["_id"]
            },{
                "$set":{
                    "activeTime": arrow.utcnow().datetime
                }
            })
    pass


