被管理起来的元数据，包括bot，bok等






# 原模型技术栈


## 验证

1. cerburus,
2. json-schema:
    1. https://github.com/Julian/jsonschema


## 引用
jsonref: https://github.com/gazpachoking/jsonref

## 合并： 

1. jsonmerge： https://github.com/avian2/jsonmerge


## yaml 

1. PyYaml,
2. ruamel(PyYaml长久不维护后衍生出来的版本)
3. yaml2json, json2yaml,jq 等命令做处理


# meta-data-xk 组织


config 配置
src 原来存放元模型的数据的地方（xk-ms，oper等可能会使用这个目录），有待切换
dst 将modle或者source编译转换后的生成目录，（用词，考虑output，build后，dest，dist后，还是使用dst）
release 将dst中生成的东西作为正式版化的发布也存在库中
mdl  model的简写，原来src的东西先复制到这里，在这个目录下整理，然后切换对src的使用（要么直接使用mdl，要么使用release）
  schema 各种类型定义的schema
  resource 各种资源定义的schema
