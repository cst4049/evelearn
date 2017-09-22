import os
import yaml

# 默认返回xml,
XML = False

# 数据库信息
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'questionbank'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {}

for file in os.listdir("schema"):
    f = open("schema"+os.path.sep+file)
    schemas = yaml.load(f)
    collection = os.path.splitext(file)[0]

    info = {
        'schema': schemas
    }

    DOMAIN.update({collection: info})
    print(DOMAIN)