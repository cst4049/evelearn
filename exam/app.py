import os

from eve import Eve
from flask_cors import CORS
from werkzeug.routing import BaseConverter

from ms.validators import MyValidator



class RegexConverter(BaseConverter):
    '''
    路由中增加支持正则表达式
    '''
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Eve(
    ## 扩展schema的定义，可使用UUID
    settings=os.path.join(os.path.dirname(os.path.abspath(__file__)),"settings/settings.py"),
    validator=MyValidator,
)

CORS(app) # 使能全部跨域
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.converters['regex'] = RegexConverter  # 增加正则表达式支持
