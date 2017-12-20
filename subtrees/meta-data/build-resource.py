from cerberus import schema_registry

import jsonmerge

from jsonref import JsonRef

import yaml

import glob

import os,sys

from config import yaml_dump_conf



DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH  = os.path.join(DIR_PATH, "mdl/resource")
SCHEMA_PATH  = os.path.join(DIR_PATH, "mdl/schema")
DST_PATH =  os.path.join(DIR_PATH, "dst")
SCHEMA_DST = os.path.join(DST_PATH, "schema.yaml")
RESOURCE_DST = os.path.join(DST_PATH, "resources.yaml")


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

# yaml.dump(doc_list[1], sys.stdout, **yaml_dump_args)
# yaml.dump(combo, sys.stdout, **yaml_dump_args)
# yaml.dump(resolved, sys.stdout, **yaml_dump_args)

with open(SCHEMA_DST,'w') as f:
    yaml.dump(resolved['definitions'], f, **yaml_dump_conf)

with open(RESOURCE_DST,'w') as f:
    yaml.dump(resolved['resources'], f, **yaml_dump_conf)
