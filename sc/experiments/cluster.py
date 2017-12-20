
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

centers = [[0, 0, 0, 8], [8, 0, 8, 0], [0, 8, 0, 0]]
columns_name = ['x1', 'x2', 'x3', 'x4']
data = pd.DataFrame()
for center in centers:
    data_temp = pd.DataFrame()
    for idx, j in enumerate(center):
        data_temp = pd.concat([data_temp, pd.DataFrame({columns_name[idx]: np.random.normal(j, size=50)})], axis=1)
    data = pd.concat([data, data_temp], ignore_index=True)

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage,dendrogram
#这里使用scipy的层次聚类函数

Z = linkage(data, method = 'ward', metric = 'euclidean') #谱系聚类图
P = dendrogram(Z, 0) #画谱系聚类图



from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
X = [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]
Z = linkage(X, 'ward')
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)

Z = linkage(X, 'single')
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)
plt.show()

plt.show()