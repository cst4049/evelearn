#遍历该目录下所有的yaml文件 将其转换为 json文件
#python -c 'import sys, yaml, json;json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)' < ./yaml/politics_bok_tree.yaml > ./json/politics_bok_tree.yaml.json
python -c '
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import  yaml, json;



fp = open("./ClassDirectionKind.json","w")
# 读取文件内容. 将其转换为yaml
file = open("./ClassDirectionKind.yaml")


a = json.dump(yaml.load(file), fp,indent=4,ensure_ascii=False)
print (a)
'