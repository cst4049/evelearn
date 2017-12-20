from cerberus import schema_registry

import jsonmerge

from jsonref import JsonRef

import yaml

import glob

import os,sys

import cerberus

from validator import MyValidator

from os.path import dirname, realpath, join
import yaml




def require(fp):
    with open(join(dirname(realpath(__file__)), fp), 'r') as f:
        d = yaml.load(f)
        return d

schema = require('dst/schema.yaml')

schema['User']




from cerberus import schema_registry
from cerberus import rules_set_registry



for k,v in schema.items():
    schema_registry.add(k, v['schema'])

v = cerberus.Validator()
v = MyValidator()


v.validate(
    {'name': 'Little Joe', 'age': 5},
    schema['User']['schema']
)


"""
demo 检查 enum
"""
v = MyValidator()
inst1 = require('mdl/instance/enum/BOKLyroEnum.yaml')
x = v.validate( inst1['instances']['BOKLyroEnum'], schema['Enum']['schema'] )

from config import yaml_dump_args
yaml.dump(inst1['instances']['BOKLyroEnum'], sys.stdout, **yaml_dump_args)
yaml.dump(schema['Enum']['schema'], sys.stdout, **yaml_dump_args)


print(v.errors)
