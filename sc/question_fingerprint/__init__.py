


# = 为题目建立多种指纹（figerprint，有的地方可能使用gsignature这个词）
# = 有使用simhash构成的、能用于表征文档相似度特征的指纹
import jieba
from pymongo import MongoClient
from bs4 import BeautifulSoup
from sc.question_fingerprint import stop_word
from sc.lsh import simhash
import os

#from jieba import analyse
#analyse.set_stop_words("stop_word.txt")
MONGO_HOST = os.environ.get("MONGO_HOST") or\
             "172.17.1.100"
URI = "mongodb://%s:27017/cb" % MONGO_HOST
Client = MongoClient(URI)
db = Client.cb
ques_col = db.questions


def beauty_cont(html):
    """
    beautifulsoup 去标签
    :param html:
    :return:
    """
    soup = BeautifulSoup(html,"html.parser")
    formula = soup.find_all("math") #todo
    return soup.get_text(),formula
    #return soup.get_text()


def participle(content):
    """
    jieba 拆分词组
    :param content:
    :return:
    """
    jieba.load_userdict(os.path.join(os.path.dirname(os.path.realpath(__file__)),"dict.txt"))
    return jieba.cut(content)


def remove_stop_word(words):
    """
    去除stop_word
    :param words:
    :return:
    """
    stop_words = stop_word.stop_words
    return (word for word in words if word not in stop_words)


def comparecode(codef,codebl,para=3):
    diff = bin(codef ^ codebl)
    diff_para = sum([int(para) for para in diff[3:]])
    if diff_para <= para:
        return True
    return False


def doall(content):
    beaut_cont,formula = beauty_cont(content)
    after_jieba = participle(beaut_cont)
    word_list = [str(i) for i in formula]
    word_list.extend(after_jieba)
    real_word = remove_stop_word(word_list)
    hashcode = simhash(real_word)
    return hashcode
