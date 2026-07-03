

from typing import Counter



file_name = 'cont-hospital/node_labels.txt'

folder = './figure/hospital/hospital'

from get_total_t_k import get_pro_result,get_random_all,get_random1,get_rand_pro_result

label_list = [0,1,2,3,4]

# AorB = 4
gap = 0.2
data = folder

edge_name = 'cont-hospital/reindexed_hyperedges.txt'
for AorB in label_list:
    result,class_propotion,k_count = get_pro_result(label_file_name=file_name,edge_file_name=edge_name,data_name=data,AorB = AorB,gap=gap)

print("k_count",k_count)
edge_name = data+ "_random_edge.txt"
node_name = data + '_random_node.txt'
get_random_all(k_count,class_propotion,edge_name,node_name)

# AorB = 4
# gap = 0.05
data_name = data+'_random'
for AorB in label_list:
    result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)

    # result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = data_name,AorB = AorB,gap=gap)

m = 0
k = []
for i in k_count:
    m+=i[1]
    k.append(i[0])


from plt_for_all import get_result,plt_all2
# # gap = 0.1
k_max = 8
gap = 0.2


result = []
result_origin = []
class_num = 5
for i in range(class_num):
    origin_A = folder +f'_{label_list[i]}_result_{gap}.txt'
    A = folder + f'_random_{label_list[i]}_result_{gap}.txt'

    result_origin.append(get_result(origin_A))
    result.append(get_result(A))
plt_all2(result,result_origin,class_num,gap,k_max,label=label_list,folder=folder,symmet=False)

# class {0: 8, 1: 28, 2: 11, 3: 29, 4: 5}
