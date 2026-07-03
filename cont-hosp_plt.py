

# from typing import Counter



# file_name = 'cont-hospital/node_labels.txt'

# folder = './figure/hospital/hospital'

# from get_total_t_k import get_pro_result,get_random_all,get_random1

# label_list = [0,1,2,3,4]

# # AorB = 4
# gap = 0.2
# data = folder

# edge_name = 'cont-hospital/reindexed_hyperedges.txt'
# for AorB in label_list:
#     result,class_propotion,k_count = get_pro_result(label_file_name=file_name,edge_file_name=edge_name,data_name=data,AorB = AorB,gap=gap)

# print("k_count",k_count)
# edge_name = data+ "_random_edge.txt"
# node_name = data + '_random_node.txt'
# get_random_all(k_count,class_propotion,edge_name,node_name)

# # AorB = 4
# # gap = 0.05
# data_name = data+'_random'
# for AorB in label_list:
#     result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = data_name,AorB = AorB,gap=gap)

# m = 0
# k = []
# for i in k_count:
#     m+=i[1]
#     k.append(i[0])
