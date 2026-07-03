# 首先读取数据
# paper ID，gender两列
# 计算ht/k
# k个点的超边中t节点属于A类的超边的个数
# 总k个节点的超边的个数

import math
import numpy as np

# 封装出来一个模式，在别的数据上做实验，写好注释
from typing import Counter

def get_node_label(file_name):
    node_label = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            node_label.append(int(line.strip()))
    node_class_count = dict(Counter(node_label))
    # print(node_class_count)
    # {1: 908, 2: 810}
    # class_propotion = node_class_count[1]/(len(node_label))

    return node_label,node_class_count

def get_hyper_edges(file_name):
    hyper_edges = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.strip().split(',')
            int_values = [int(value) for value in values]
            hyper_edges.append(int_values)
    return hyper_edges
# hyper_edges = get_hyper_edges('./original-data/congress-bills/hyperedges-test.txt')

def h_t_k(feature):
    for t_k in feature:
        t_k.append(t_k[1]/t_k[0])
        # t_k
    return feature
def in_txt(file_name,data):
    lines = [','.join(map(str, row)) for row in data]
    # 打开文本文件并写入数据
    with open(file_name, 'w') as file:
        for line in lines:
            file.write(line + '\n')
from collections import Counter

def get_edge_class(hyper_edges,node_label,AorB):
    feature = []
    total_hyperclass = []
    k_max = 0

    for edge in hyper_edges:
        node_class = []
        t = 0
        for node in edge:
            label = node_label[node-1]
            node_class.append(label)
            if label == AorB:
                t += 1
        if len(edge)>k_max:
            k_max = len(edge)
        total_hyperclass.append(node_class)
        feature.append([len(edge),t])

    feature = h_t_k(feature)
    feature = sorted(feature, key=lambda x: (x[0],x[1]))
    count = Counter([item[0] for item in feature])
    count = count.most_common()
    return total_hyperclass,feature,k_max,count


def count_kt_pairs(matrix, k, t):
    element_pairs = [(sublist[0], sublist[1]) for sublist in matrix if len(sublist) >= 2]
    counter = Counter(element_pairs)
    return counter[(k, t)]


def get_over(feature,value,k,gap):
    propotion = 0
    for t in range(k+1):
        pro = t/k
        if pro >= value-1e-10 and pro <= value+gap+1e-10:
            result = count_kt_pairs(feature, k, t)
            propotion += result
    return propotion
def get_diff(result):
    result.append(0)
    result = [result[i]-result[i+1] for i in range(len(result)-1)]
    
    return result
def get_pro_result(label_file_name,edge_file_name,data_name,AorB = 1,gap = 0.05):
    r = []
    node_label,class_propotion = get_node_label(label_file_name)
    print("class",class_propotion)
    num_bins = int(1/gap)
    hyper_edges = get_hyper_edges(edge_file_name)
    _,feature,k_max,k_count = get_edge_class(hyper_edges,node_label,AorB=AorB)
    for k_num in k_count:
        s_r = [k_num[0]]
        for value in range(num_bins):
            s_r.append(get_over(feature,value*gap,k_num[0],gap))
        r.append(s_r)
    result = []
    for col in range(1,len(r[0])):
        col_sum = 0
        total = 0
        for row in range(len(r)):
            col_sum += r[row][col]
        result.append(col_sum)
    total = sum(pair[1] for pair in k_count)
    result = [item / total for item in result]
    print(result)
    file_name = f'{data_name}_{AorB}_result_{gap}.txt'
    with open(file_name, 'w') as file:
        for item in result:
            file.write(str(item) + '\n')
    return result,class_propotion,k_count

def get_rand_pro_result(k_count,class_propotion,data_name,AorB = 1,gap = 0.05):
    r = []
    def get_frac(value,k,gap):
        numerator = 0
        # node_num = 0
        node_num = sum(class_propotion.values())
        denominator = math.comb(node_num,k)
        for t in range(k+1):
            pro = t/k
            if pro >= value-1e-5 and pro <= value+gap+1e-5:
                numerator += math.comb(class_propotion[AorB], t)*math.comb(node_num-class_propotion[AorB],k-t)
        return numerator/denominator

    total = sum(pair[1] for pair in k_count)
    for k_num in k_count:
        s_r = [k_num[0]]
        for value in np.arange(0,1,gap):
            s_r.append(get_frac(value,k_num[0],gap)*k_num[1]/total)
        r.append(s_r)
    print(r)
    result = []
    for col in range(1,len(r[0])):
        col_sum = 0
        for row in range(len(r)):
            col_sum += r[row][col]
        result.append(col_sum)
    file_name = f'{data_name}_{AorB}_result_{gap}.txt'
    with open(file_name, 'w') as file:
        for item in result:
            file.write(str(item) + '\n')
    return result,class_propotion,k_count

import random

def get_random(s,class_propotion,edge_name,node_name):
    vertices = class_propotion[1] + class_propotion[2]
    random_hyperedge = []

    # 重复100次
    results = []
    for _ in range(100):
        temp_hyperedge = []
        for couple in s:
            for i in range(couple[1]):
                random_selection = random.sample(range(1, vertices + 1), couple[0])
                temp_hyperedge.append(random_selection)
        results.append(temp_hyperedge)

    # 计算所有结果的平均值
    average_hyperedge = []
    for i in range(len(results[0])):
        # 对每个位置的结果取平均
        avg_selection = [sum(result[i][j] for result in results) / 100 for j in range(len(results[0][i]))]
        # 对平均值取整
        avg_selection = [math.floor(x) for x in avg_selection]
        average_hyperedge.append(avg_selection)

    random_hyperedge = average_hyperedge
    vertices = class_propotion[1]+class_propotion[2]
    random_hyperedge = []
    for couple in s:
        for i in range(couple[1]):
            random_selection = random.sample(range(1,vertices+1),couple[0])
            random_hyperedge.append(random_selection)
    in_txt(edge_name,random_hyperedge)
    node = [1]*class_propotion[1]+[2]*class_propotion[2]
    with open(node_name, 'w') as file:
        for item in node:
            file.write(str(item) + '\n')


def get_random_all(s,class_propotion,edge_name,node_name):
    print(len(class_propotion))
    vertices = 0
    for i in range(len(class_propotion)):
        # vertices += class_propotion[i+1]
        vertices += class_propotion[i]
    random_hyperedge = []

    # 重复100次
    results = []
    for _ in range(100):
        temp_hyperedge = []
        for couple in s:
            for i in range(couple[1]):
                random_selection = random.sample(range(1, vertices + 1), couple[0])
                temp_hyperedge.append(random_selection)
        results.append(temp_hyperedge)

    # 计算所有结果的平均值
    average_hyperedge = []
    for i in range(len(results[0])):
        # 对每个位置的结果取平均
        avg_selection = [sum(result[i][j] for result in results) / 20 for j in range(len(results[0][i]))]
        # 对平均值取整
        avg_selection = [math.floor(x) for x in avg_selection]
        average_hyperedge.append(avg_selection)

    random_hyperedge = average_hyperedge
    # vertices = class_propotion[1]+class_propotion[2]
    random_hyperedge = []
    for couple in s:
        for i in range(couple[1]):
            random_selection = random.sample(range(1,vertices+1),couple[0])
            random_hyperedge.append(random_selection)
    in_txt(edge_name,random_hyperedge)
    node = []
    for i in range(len(class_propotion)):
        node += [i]*class_propotion[i]
    with open(node_name, 'w') as file:
        for item in node:
            file.write(str(item) + '\n')


def get_random1(s,class_propotion,edge_name,node_name):
    vertices = class_propotion[1] + class_propotion[2]+class_propotion[3]+class_propotion[4]
    random_hyperedge = []

    # 重复100次
    results = []
    for _ in range(20):
        temp_hyperedge = []
        for couple in s:
            for i in range(couple[1]):
                random_selection = random.sample(range(1, vertices + 1), couple[0])
                temp_hyperedge.append(random_selection)
        results.append(temp_hyperedge)

    # 计算所有结果的平均值
    average_hyperedge = []
    for i in range(len(results[0])):
        # 对每个位置的结果取平均
        avg_selection = [sum(result[i][j] for result in results) / 20 for j in range(len(results[0][i]))]
        # 对平均值取整
        avg_selection = [math.floor(x) for x in avg_selection]
        average_hyperedge.append(avg_selection)

    random_hyperedge = average_hyperedge
    vertices = class_propotion[1]+class_propotion[2]+class_propotion[3]+class_propotion[4]
    random_hyperedge = []
    for couple in s:
        for i in range(couple[1]):
            random_selection = random.sample(range(1,vertices+1),couple[0])
            random_hyperedge.append(random_selection)
    in_txt(edge_name,random_hyperedge)
    node = [1]*class_propotion[1]+[2]*class_propotion[2]+[3]*class_propotion[3]+[4]*class_propotion[4]
    with open(node_name, 'w') as file:
        for item in node:
            file.write(str(item) + '\n')
