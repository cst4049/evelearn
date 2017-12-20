from ms.settings.settings_base import *


MONGO_HOST = os.environ.get('MONGO_HOST') or \
            '127.0.0.1'
MONGO_PORT =  27017
MONGO_DBNAME = 'cb'