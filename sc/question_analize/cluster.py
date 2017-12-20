
import numpy as np
from numpy import array
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import fcluster
import sys
sys.path.append("../../")
from sc.question_fingerprint import ques_col
import yaml
import os
import datetime



def question_cluster(questions, verbose=False, format='groupid',max_d=4):
    """ 将题目按照simhash之间的海明距离聚类

    >>> questions = [{'simhash': 1},{'simhash': 2}, {'simhash': 3 },{'simhash': 100},{'simhash': 101}, {'simhash': 1000 }]
    >>> question_cluster(questions,verbose=False)
    [1, 1, 1, 2, 2, 3]

    format=grouped
    [[0,1,2],[3,4],[5]]
    """
    print(max_d)
    simhashes = [ int(str(q['simhash'])) for q in questions]

    # - 算距离矩阵

    def h(x, y):
        return bin(np.bitwise_xor(np.rint(x[0]).astype(np.int64), np.rint(y[0]).astype(np.int64))).count('1')

    bits = [ 1 << i for i in range(64) ]
    X = [[x & bits[i] for i in range(64)] for x in simhashes]
    dist_matrix = distance.pdist(
        array(X, dtype=np.uint64),
        metric='hamming'
    )
    if (verbose):
        print(dist_matrix*64)
        print(distance.squareform(dist_matrix*64))

    # - 根据距离矩阵算聚类关系

    Z = linkage(dist_matrix*64, 'single')
    if(verbose):
        # fig = plt.figure(figsize=(25, 10))
        # dn = dendrogram(Z)
        # plt.show()
        pass

    # - 根据聚类，指定最大距离，形成分组划分

    clusters = fcluster(Z, max_d, criterion='distance')
    if (verbose):
        print(clusters)

    if format == 'groupid':
        return clusters
    if format == 'grouped':
        partition = [list(np.where(clusters == i)[0]) for i in range(clusters.min(), clusters.max() + 1)]
        duplicated_set = [i for i in partition if len(i) > 1]
        for i in duplicated_set:
            print(i)
        l1 = []
        base_dir = "/tmp/simhash" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        for i, v in enumerate(duplicated_set):
            file_name = base_dir + "/simhash" + str(i) + ".yaml"
            l2 = []
            for q in v:
                questions[q]["_id"] = str(questions[q]["_id"])
                questions[q]["simhash"] = str(questions[q]["simhash"])
                l2.append(questions[q])
            with open(file_name, 'w') as f:
                yaml.dump(l2, f, allow_unicode=True, indent=4)
        return  partition


if __name__ == '__main__':
    from timeit import timeit

    #questions = [{'simhash': 1}, {'simhash': 2}, {'simhash': 3}, {'simhash': 100}, {'simhash': 101}, {'simhash': 1000}]
    questions = list(ques_col.find({"simhash":{"$exists":True}},{"simhash":1,"contOfQuery":1}))

    # for k,f in enumerate([question_cluster]):
        #print('1000 * {:<20}'.format(f.__name__), timeit(lambda: f(questions), number=1000))

    aa = question_cluster(questions,verbose=True,format='grouped',max_d=4)