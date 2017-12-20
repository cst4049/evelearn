
# = 题目相似度，题目限定了业务领域，相似度定义了科学计算的方面
# = 具体有题目的 simhash 计算 与比较
# = 具体有题目的 两两相比的 编辑距离
# = 不默认设置数据库的链接，题目根据 simhash查找的逻辑封装到 题目模型中


def simhash(question_query_content):
    """ 题目内容的simhash值（64位）
    >>> content = '我是一个物理题，关于球体滚动'
    >>> simhash(content)


    """
    pass

def levenshtein(question_query_content1, question_query_content2):
    """ 两道题目内容的编辑距离
    >>> content1 = '我是一个物理题，关于球体滚动'
    >>> content1 = '我是一个物理题，关于球体运动'
    >>> levenshtein(content1,content2)


    """
    pass