#!/usr/bin/python
# -*-coding:utf-8-*-

from  initial import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import loadmat

random.seed(1)
np.random.seed(1)


#解决中文显示问题
plt.rcParams['font.sans-serif']=['KaiTi']
plt.rcParams['axes.unicode_minus'] = False

"""  
    函数功能：寻找每个样本距离最近的中心点  
    X: 数据集 
    centroids: 初始聚类中心个数
"""


def find_closest_centroids(X, centroids):
    m = X.shape[0]
    k = centroids.shape[0]
    # 初始每个样本的对应类别的索引值
    idx = np.zeros(m)
    # 误差平方和SSE
    sse = 0
    # 遍历整个数据集
    for i in range(m):
        # 初始最小距离 设定一个很大的值
        min_dist = 1000000
        # 对于每个初始中心点
        for j in range(k):
            # 计算样本与中心点的距离
            dist = np.sum((X[i, :] - centroids[j, :]) ** 2)
            # 如果距离小于当前最小距离
            if dist < min_dist:
                # 最小距离更新为该距离
                min_dist = dist
                # 更新该样本的类别索引值为该中心点
                idx[i] = j
        # 计算SSE值
        sse += min_dist
    return idx, sse


"""  
    函数功能：更新中心点  
    X: 数据集 
    idx：样本对应类别的索引值
    k：中心点个数
"""


def compute_centroids(X, idx, k):
    m, n = X.shape
    # 初始聚类中心（k，n）的零数组
    centroids = np.zeros((k, n))
    # 对于每个中心点
    for i in range(k):
        # 对于当前中心点类别
        indices = np.where(idx == i)
        # 更新其中心点为所有属于该类别的样本点的质心
        centroids[i, :] = (np.sum(X[indices, :], axis=1) / len(indices[0])).ravel()
    # 返回更新后的中心点
    return centroids


"""  
    函数功能：运行k-means聚类算法  
    X: 数据集 
    initial_centroids：初始聚类中心
    max_iters：最大迭代次数
"""


def run_k_means(X, initial_centroids, max_iters):
    global sse
    m, n = X.shape
    k = initial_centroids.shape[0]
    idx = np.zeros(m)
    # 随机的初始聚类中心
    centroids = initial_centroids

    for i in range(max_iters):
        # 为每个样本寻找距离最近的中心点
        idx, sse = find_closest_centroids(X, centroids)
        # 更新中心点
        centroids = compute_centroids(X, idx, k)

    return idx, centroids, sse


#加载数据集
data = loadmat('data/data2.mat')
data2 = pd.DataFrame(data.get('X'), columns=['X1', 'X2'])
X = data['X']
m = X.shape[0]
points = []
for i in range(m):
    points.append(X[i,:])

#输入的20表示的是聚类的个数，134
incenter= np.array(initCenters(points,m,2))
print('聚类中心为：incenter:',incenter)

initial_centroids = incenter
idx, centroids,sse = run_k_means(X, initial_centroids, 4)
# print('centroids:',centroids)
print('误差平方和SSE=',sse)
# plt.figure(figsize=[15,8])
data2['C'] = idx
#print(data2)
sns.lmplot('X1', 'X2', hue='C', data=data2, fit_reg=False,legend=False)
plt.title('时空扫描模型簇类中心与K-means区域聚类投影',size=15)
# plt.scatter(x=centroids[:,0],y=centroids[:,1],c='r',marker='x')
# plt.legend(loc=1)
plt.xlabel('经度',size=15)
plt.ylabel('纬度',size=15)
plt.yticks(fontproperties = 'Times New Roman', size = 13)
plt.xticks(fontproperties = 'Times New Roman', size = 13)

# ax=plt.gca();#获得坐标轴的句柄
# ax.spines['bottom'].set_linewidth(2);###设置底部坐标轴的粗细
# ax.spines['left'].set_linewidth(2);####设置左边坐标轴的粗细
#时空扫描簇类中心
XX=[34.78339, 34.79536, 34.78331, 34.76939, 34.8346, 34.76125, 34.80035, 34.80215, 34.760619, 34.81693, 34.76894, 34.7802, 34.77672, 34.75712, 34.76602, 34.78334, 34.774964, 34.79317, 34.84021, 34.81855, 34.7496, 34.81139, 34.80934, 34.80099, 34.74612, 34.78974, 34.77272]
YY=[32.09556, 32.08372, 32.12094, 32.06719, 32.12329, 32.04625, 32.12786, 32.04625, 32.054935, 32.11941, 32.07577, 32.066, 32.05647, 32.0376, 32.05299, 32.07991, 32.08437, 32.06652, 32.11176, 32.1111, 32.03869, 32.057, 32.12327, 32.05472, 32.0321, 32.08527, 32.05038]
# plt.scatter(XX,YY,color='r',s=1000,alpha=0.3)
# plt.scatter(XX,YY,color='black',s=50)
plt.scatter(XX,YY,color='black',s=50,marker='*')

# plt.legend(["K-means","Scanter"])

plt.tight_layout()

plt.savefig('./result.jpg',dpi=100)
plt.show()
