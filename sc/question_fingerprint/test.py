from sc.question_fingerprint import doall
import yaml

with open("./test-data/should_be_different.yaml") as f:
    data = yaml.load(f)
    l=[]
    for ques in data[0]:
        code = doall(ques.get("contOfQuery"))
        print(code)
        aa= bin(code)
        print(aa)
        l.append(aa)
    print(bin(eval(l[0])^eval(l[1])))