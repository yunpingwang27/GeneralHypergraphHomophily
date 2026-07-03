
from typing import Counter

def get_node_label(file_name):
    node_label = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            label = int(line.strip())
            if label==7:
                node_label.append(1)
            elif label == 8:
                node_label.append(2)
            elif label == 1:
                node_label.append(3)
            else:
                node_label.append(4)
    node_class_count = dict(Counter(node_label))
    return node_label,node_class_count

node_label_name = 'original-data/walmart-trips/node-labels-walmart-trips.txt'
# node_label_name = 'original-data/contact-high-school-classes-gender/node-labels-contact-high-school-classes-gender.txt'
node_label,class_count = get_node_label(node_label_name)
def in_label_txt(node_label,file_name):
    with open(file_name, 'w') as file:
        for item in node_label:
            file.write(str(item) + '\n')
file_name = 'original-data/node-labels-get.txt'
in_label_txt(node_label,file_name)


from get_total_t_k import get_pro_result,get_random1,get_rand_pro_result

AorB = 1
gap = 0.1
data = './figure/walmart/walmart'
# file_name = node_label_name
label_name = 'original-data/contact-primary-school-classes-gender/node-labels-get.txt'
edge_name = 'original-data/walmart-trips/hyperedges-walmart-trips.txt'
# edge_name = 'original-data/contact-high-school-classes-gender/hyperedges-contact-high-school-classes-gender.txt'
result,class_propotion,k_count = get_pro_result(label_file_name=file_name,edge_file_name=edge_name,data_name=data,AorB = AorB,gap=gap)
# print(k_count)
AorB = 2
# gap = 0.1
result,class_propotion,k_count = get_pro_result(label_file_name =file_name,edge_file_name = edge_name,data_name=data,AorB = AorB,gap=gap)

AorB = 3
result,class_propotion,k_count = get_pro_result(label_file_name =file_name,edge_file_name = edge_name,data_name=data,AorB = AorB,gap=gap)

print("k_count",k_count)
edge_name = data+ "_random_edge.txt"
node_name = data + '_random_node.txt'
get_random1(k_count,class_propotion,edge_name,node_name)
AorB = 1
# gap = 0.05
data_name = data+'_random'
result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)
AorB = 2
result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)
AorB = 3
result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)

# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = data_name,AorB = AorB,gap=gap)
# AorB = 2
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)
# AorB = 3
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)

# print(class_propotion)
# print(k_count)
# print(class_propotion)
# print(k_count)
m = 0
k = []
for i in k_count:
    m+=i[1]
    k.append(i[0])
# print(max(k))
# print(m)
# print(class_propotion[1]+class_propotion[2])

from plt_for_all import get_result,plt_all1
gap = 0.1
# k_max = k_count[-1][0]
# print(k_max)
k_max = 25
folder = data
origin_A = folder +f'_1_result_{gap}.txt'
origin_B = folder +f'_2_result_{gap}.txt'

origin_C = folder +f'_3_result_{gap}.txt'
A = folder + f'_random_1_result_{gap}.txt'
B = folder + f'_random_2_result_{gap}.txt'
C = folder + f'_random_3_result_{gap}.txt'

result_origin_A = get_result(origin_A)
result_origin_B = get_result(origin_B)
result_origin_C = get_result(origin_C)
result_A = get_result(A)
result_B = get_result(B)
result_C = get_result(C)
plt_all1(result_A,result_B,result_C,result_origin_A,result_origin_B,result_origin_C,gap,k_max,label=['Food, Household & Pets',"Pharmacy, Health & Beauty","Clothing, Shoes & Accessories"],folder=folder,symmet=False)

