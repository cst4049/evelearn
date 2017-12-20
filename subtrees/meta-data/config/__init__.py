
from os.path import dirname, realpath, join
import yaml




def require(fp):
    with open(join(dirname(realpath(__file__)), fp), 'r') as f:
        d = yaml.load(f)
        return d

yaml_dump_conf = require('yaml-dump-conf.yaml')
yaml_dump_args = yaml_dump_conf
