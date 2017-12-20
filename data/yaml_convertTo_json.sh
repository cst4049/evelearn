#遍历该目录下所有的yaml文件 将其转换为 json文件
#python -c 'import sys, yaml, json;json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)' < ./yaml/politics_bok_tree.yaml > ./json/politics_bok_tree.yaml.json
python -c '
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import  yaml, json;
import time

start_time = time.time()

fileList = os.listdir("./yaml")
try:
    os.mkdir("./json")
except:
    print("json目录已经存在")
try:
    os.mkdir("./json/bot")
except:
    print("bot目录已经存在")
try:
    os.mkdir("./json/bok")
except:
    print("bok目录已经存在")


for item in fileList:

    # 读取文件内容. 将其转换为yaml
    file = open("./yaml/"+item)
    if "bok" in item:
        fp = open("./json/bok/json_" + item, "w")
        f = open("./json/bok/json_" + item, "r+")
    else:
        fp = open("./json/bot/json_" + item, "w")
        f = open("./json/bot/json_" + item, "r+")

    json.dump(yaml.load(file), fp,indent=4,ensure_ascii=False)
    file.close()
    fp.close()

    # 将null 替换成 []
    all_lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in all_lines:
        line = line.replace("null","[]")
        f.write(line)
    f.close()
end_time = time.time()
print(end_time - start_time)
'