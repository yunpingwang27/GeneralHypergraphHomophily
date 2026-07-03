def get_label_index(file_name):
    hyper_edges = []
    label_index = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.strip().split(' ')
            # int_values = [value for value in values]
            hyper_edges.append(values[1])
            if values[1] == 'M':
                label_index.append(1)
            elif values[1] == 'F':
                label_index.append(2)
            else:
                label_index.append(3)
    return label_index
label_index_name = 'original-data/contact-high-school-classes-gender/label-names-contact-high-school-classes-gender.txt'
label_index = get_label_index(label_index_name)
# print(label_index)
from typing import Counter
def get_node_label(file_name,label_index):
    node_label = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            label = int(line.strip())
            node_label.append(label_index[label-1])
    node_class_count = dict(Counter(node_label))
    return node_label,node_class_count
node_label_name = './original-data/contact-high-school-classes-gender/node-labels-contact-high-school-classes-gender.txt'
node_label,class_count = get_node_label(node_label_name,label_index)
print(node_label)
def in_label_txt(node_label,file_name):
    with open(file_name, 'w') as file:
        for item in node_label:
            file.write(str(item) + '\n')
file_name = './original-data/contact-high-school-classes-gender/node-labels-get.txt'
in_label_txt(node_label,file_name)

from get_total_t_k import get_pro_result,get_random_all,get_random,get_rand_pro_result

AorB = 1
gap = 0.2
data = './figure/high/high'
label_name = './original-data/contact-primary-school-classes-gender/node-labels-get.txt'
edge_name = './original-data/contact-high-school-classes-gender/hyperedges-contact-high-school-classes-gender.txt'
result,class_propotion,k_count = get_pro_result(label_file_name=file_name,edge_file_name=edge_name,data_name=data,AorB = AorB,gap=gap)
# print(k_count)
AorB = 2
# gap = 0.1
result,class_propotion,k_count = get_pro_result(label_file_name =file_name,edge_file_name = edge_name,data_name=data,AorB = AorB,gap=gap)

# print(result)
edge_name = data+ "_random_edge.txt"
node_name = data + '_random_node.txt'
get_random(k_count,class_propotion,edge_name,node_name)
AorB = 1
# gap = 0.05
data_name = './figure/high/high_random'
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = data_name,AorB = AorB,gap=gap)
# AorB = 2
result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)

AorB = 2
result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)

# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)
print(class_propotion)
print(k_count)

from plt_for_all import get_result,plt_all
# gap = 0.1
k_max = 5
folder = './figure/high/high'
origin_A = folder +f'_1_result_{gap}.txt'
origin_B = folder +f'_2_result_{gap}.txt'
A = folder + f'_random_1_result_{gap}.txt'
B = folder + f'_random_2_result_{gap}.txt'
result_origin_A = get_result(origin_A)
result_origin_B = get_result(origin_B)
result_A = get_result(A)
result_B = get_result(B)
plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label=['Male','Female'],folder=folder,symmet=False)
print(class_propotion)
print(k_count)
m=0
k = []
for i in k_count:
    m+=i[1]
    k.append(i[0])
print(max(k))

print(m)
print(class_propotion[1]+class_propotion[2])

