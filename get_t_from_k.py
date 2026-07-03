# 首先读取数据
# paper ID，gender两列
# 计算ht/k
# k个点的超边中t节点属于A类的超边的个数
# 总k个节点的超边的个数
from typing import Counter


node_label = []
with open('./original-data/congress-bills/node-labels-congress-bills.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        # print(line.strip())  # 使用strip()方法去除每行末尾的换行符
        node_label.append(int(line.strip()))
# print(node_label[0:10])
hyper_edges = []
with open('./original-data/congress-bills/hyperedges-test.txt', 'r') as file:
    lines = file.readlines()
    # data_line = []
    for line in lines:
        values = line.strip().split(',')
        int_values = [int(value) for value in values]
        hyper_edges.append(int_values)
        # print(line.strip())  # 使用strip()方法去除每行末尾的换行符
        # node_label.append(int(line.strip()))
# print(hyper_edges[0:10])
feature = []
total_hyperclass = []
k_list = []
t_list = []
for edge in hyper_edges:
    node_class = []
    # feature = []
    t = 0
    for node in edge:
        label = node_label[node-1]
        node_class.append(label)
        if label == 1:
            t += 1
    total_hyperclass.append(node_class)
    feature.append([len(edge),t])
    k_list.append(len(edge))
    t_list.append(t)
# print(feature[0:10])
# print(total_hyperclass[0:10])     
node_class_count = dict(Counter(node_label))
print(node_class_count)
def in_txt(file_name,data):
    lines = [','.join(map(str, row)) for row in data]

    # 打开文本文件并写入数据
    with open(file_name, 'w') as file:
        for line in lines:
            file.write(line + '\n')


in_txt('hyperedge_class.txt',total_hyperclass)

def h_t_k(feature):
    for t_k in feature:
        t_k.append(t_k[1]/t_k[0])
        # t_k
    return feature

feature = h_t_k(feature)
feature = sorted(feature, key=lambda x: (x[0],x[1]))
in_txt('feature.txt',feature)
s = dict(Counter(k_list))

# Counter()
from collections import Counter

def count_kt_pairs(matrix, k, t):
    element_pairs = [(sublist[0], sublist[1]) for sublist in matrix if len(sublist) >= 2]
    counter = Counter(element_pairs)
    return counter[(k, t)]

import math

def b_t_k(k,t,propotion):
    s = math.comb(k,t)
    b_t = propotion ** t
    b_t *= (1-propotion) ** (k-t)
    b_t *= s
    return b_t
# b_t_k
class_propotion = node_class_count[1]/(len(node_label))

def ht_bt(k,t,h_t,propotion):
    pro = b_t_k(k,t,propotion)
    pro = h_t/pro
    return pro

t_k_pro = []

r = []
import numpy as np
def get_over(value,k):
    # s = [k]
    propotion = 0
    for t in range(k+1):
        pro = t/k
        if pro >= value:
            result = count_kt_pairs(feature, k, t)
            propotion += result
            # s.append(propotion)
    return propotion

# print(k_list)
from scipy.stats import norm

# 指定均值（mean）和标准差（stddev）参数
node_A = 908
node_B = 810
mean = node_A/(node_A+node_B)
std_dev = math.sqrt(mean*(1-mean))


# 要计算的值
# x = 0.75

def get_cdf_pro(x):
# 计算对应值的CDF
    probability = norm.cdf(x, loc=mean, scale=std_dev)
    return(probability)
probability = []
index = []
# for value in np.arange(0,1.1,0.1):
for value in np.arange(0,1.1,0.1):
    index.append(value)
    probability.append(get_cdf_pro(1-value))
# print(probability)
# print(index)
# print("CDF值为:", probability)
r = []
# 正态分布求积分对应的均值，0.1，0.2,0.3……，得到对应的t/k
# 当对应的t/k时实际的概率情况

for k in range(2,26):
    s_r = [k]
    # index = ['k']
    s_r.append(get_over(0,k))
    for pro in index:
        print(pro)
        # index.append()
        s_r.append(get_over(pro,k))
    r.append(s_r)
# print(r)
result = []
pro_result = []
for col in range(2,len(r[0])):
    col_sum = 0
    total = 0
    # 遍历每一行，并将对应位置的元素相加
    for row in range(len(r)):
        total += r[row][1]
        col_sum += r[row][col]
    result.append(col_sum)
    pro_result.append(col_sum/total)
# print(result)
print(pro_result)
