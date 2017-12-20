import jsonmerge
from jsonref import JsonRef
import yaml
import glob
import os

# 默认返回xml,
XML = False

# 数据库信息


MONGO_HOST = os.environ.get('MONGO_HOST')

# 192.168.146.136
# 172.17.9.10
MONGO_PORT = int(os.environ.get('MONGO_PORT')) if \
                     os.environ.get('MONGO_PORT') else 27017
MONGO_DBNAME = 'cb'

#负载均衡的设置
SCHEME = os.environ.get("SCHEME") or "http"
LDB_HOST = os.environ.get("LDB_HOST")
LDB_PORT = os.environ.get("LDB_PORT") or 80

LDB_URI = LDB_HOST + ":" + LDB_PORT if LDB_HOST and LDB_PORT else None

SCHEMA_ENDPOINT="schema"




# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST','DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# Enabled documents version control when True
VERSIONING = True

# oplog
OPLOG = True
OPLOG_ENDPOINT = 'oplog'

# Enables / Disables global the possibility to override
# the sent method with a header X-HTTP-METHOD-OVERRIDE.
ALLOW_OVERRIDE_HTTP_METHOD = True

# True to enable concurrency control, False otherwise. Defaults to True
IF_MATCH = False

# Controls the embedding of the media type in the endpoint response.
# This is useful when you have other means of getting the binary
# (like custom Flask endpoints) but still want clients to be able to
# POST/PATCH it. Defaults to True
RETURN_MEDIA_AS_BASE64_STRING = False

# 	Set it to True to enable serving media files at a dedicated
# media endpoint. Defaults to False.
RETURN_MEDIA_AS_URL = True

# If set to True, multiple values sent with the same key, submitted
# using the application/x-www-form-urlencoded or multipart/form-data
# content types, will
AUTO_COLLAPSE_MULTI_KEYS = True

# When submitting a non list type value for a field with type list,
# automatically create a one element list before running the validators.
# Defaults to False
AUTO_CREATE_LISTS = True

# Enables soft delete when set to True
SOFT_DELETE = True

# Hypermedia as the Engine of Application State
HATEOAS = False

# DATE_CREATED = "typewritedAtFirstly"
# LAST_UPDATED = "typewritedAtLastly"

# CORS (Cross-Origin Resource Sharing) support. Allows API maintainers
# to specify which domains are allowed to perform CORS requests.
# Allowed values are: None, a list of domains, or '*' for a wide-open API. Defaults to None.
X_DOMAINS = '*'

X_HEADERS = ['Content-Type']

# sleep time s/秒
DEBUG_DELAY = 0

# 重题检测默认题目数
SIMILAR_COUNT = 5

# cache
CACHE_CONTROL = 'no-cache'



DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RESOURCE_PATH  = os.path.join(DIR_PATH, "endpoints")
SCHEMA_PATH  = os.path.join(DIR_PATH, "schema")

merge_schema = {
    "properties":{
        "definitions":{
            "mergeStrategy":"objectMerge"
        },
        "resources": {
            "mergeStrategy": "objectMerge"
        }
    }
}

merger = jsonmerge.Merger(merge_schema)

schemas = {}
for file in glob.glob(os.path.join(RESOURCE_PATH, "**/*.yaml"), recursive=True):
    with open(file, 'r') as f:
        d = yaml.load(f)
        schemas = merger.merge(schemas, d)

resources = {}
for file in glob.glob(os.path.join(SCHEMA_PATH, "**/*.yaml"), recursive=True):
    with open(file, 'r') as f:
        d = yaml.load(f)
        resources = merger.merge( resources, d)

allinone = merger.merge(schemas, resources)

resolved = JsonRef.replace_refs(
    allinone,
    base_uri = 'https://rawstonedu.com/schema'
    )

DOMAIN = resolved.get("resources")


def merge_definitions(path, globpatterm):
    """
    >>> len( merge_definitions('/tmp/a', '**/*.yaml').items())
    0
    >>> len( merge_definitions(['/tmp/a','/tmp/b'], '**/*.yaml').items())
    0
    不知道单个文件的用处，暂时不填加单文件，只有文件列表
    :param path:
    :return:
    """
    merge_schema = {
        "properties": {
            "definitions": {
                "mergeStrategy": "objectMerge"
            },
            "resources": {
                "mergeStrategy": "objectMerge"
            }
        }
    }

    merger = jsonmerge.Merger(merge_schema)
    allinone = {}
    if isinstance(path,list):
        for path_define in path:
            data = {}
            for file in glob.glob(os.path.join(path_define, "**/*.yaml"), recursive=True):
                with open(file, 'r') as f:
                    d = yaml.load(f)
                    data = merger.merge(data, d)
            allinone = merger.merge(allinone, data)

        resolved = JsonRef.replace_refs(
            allinone,
            base_uri='https://rawstonedu.com/schema'
        )
        return resolved
    else:
        # 单个文件时，直接应该是endpoint + schema
        resolved = {}
        resources = {}
        for file in glob.glob(os.path.join(path, "*.yaml")):
            with open(file, 'r') as f:
                d = yaml.load(f)
                resources = merger.merge(resources, d)
            resolved.update(resources=resources)
        return resolved
resolved = merge_definitions([RESOURCE_PATH,SCHEMA_PATH],'**/*.yaml')
DOMAIN = resolved.get("resources")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
