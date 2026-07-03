# 考虑基于原图的随机图，
# 节点个数对应一样 
# 边的个数对应相等且k的分布也类似
# 
# 节点情况：{1: 908, 2: 810}
# 1718
# 给出k的情况
import random
# random.seed(42)0
s = []
def in_txt(file_name,data):
    lines = [','.join(map(str, row)) for row in data]

    # 打开文本文件并写入数据
    with open(file_name, 'w') as file:
        for line in lines:
            file.write(line + '\n')
# hyper_edges = []
with open('t_k_num.txt', 'r') as file:
    lines = file.readlines()
    # data_line = []
    for line in lines:
        values = line.strip().split(',')[:2]
        int_values = [int(value) for value in values]
        s.append(int_values)
print(s)
vertices = range(1718)
random_hyperedge = []
for couple in s:
    for i in range(couple[1]):
        random_selection = random.sample(vertices,couple[0])
        random_hyperedge.append(random_selection)
# print(random_hyperedge[793])
in_txt('random_hyperedges.txt',random_hyperedge)

node = [1]*908+[2]*810
with open('random_node.txt', 'w') as file:
    for item in node:
        file.write(str(item) + '\n')
# print(result)
