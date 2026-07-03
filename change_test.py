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
        node_label.append(int(line.strip()))
hyper_edges = []
with open('./original-data/congress-bills/hyperedges-test.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        values = line.strip().split(',')
        int_values = [int(value) for value in values]
        hyper_edges.append(int_values)
feature = []
total_hyperclass = []
k_list = []
t_list = []
for edge in hyper_edges:
    node_class = []
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
class_propotion = node_class_count[1]/(len(node_label))

def ht_bt(k,t,h_t,propotion):
    pro = b_t_k(k,t,propotion)
    pro = h_t/pro
    return pro

t_k_pro = []

r = []
import numpy as np
def get_over(value,k):
    propotion = 0
    for t in range(k+1):
        pro = t/k
        if pro >=value:
            result = count_kt_pairs(feature, k, t)
            propotion += result/s[k]
    return propotion
r = []

for k in range(1,26):
    s_r = [k]
    index = ['k']
    for value in np.arange(0.5,1,0.05):
        index.append(value)
        s_r.append(get_over(value,k))
    r.append(s_r)
r = [index]+r
print(r)
in_txt('t_k_ge_propotion.txt',r)
