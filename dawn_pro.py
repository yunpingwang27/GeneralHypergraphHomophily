# 带进度显示的版本
total_numbers = 364

with open('DAWN\labels.txt', 'w', encoding='utf-8') as file:
    for i in range(1, total_numbers + 1):
        file.write(str(i) + '\n')
        # 每50个数字显示一次进度
        if i % 50 == 0:
            print(f"已生成 {i}/{total_numbers} 个数字")

print(f"文件创建完成！共生成 {total_numbers} 个数字")
label_index_name = 'DAWN\labels.txt'

# 简洁版本




# # print(label_index)
from typing import Counter



# # from get_total_t_k import get_pro_result,get_random_all,get_random1
file_name = 'DAWN\DAWN-node_label.txt'

folder = './figure/dawn/dawn'
# # origin_A = folder +f'_1_result_{gap}.txt'
# # origin_B = folder +f'_2_result_{gap}.txt'
# # A = folder + f'_random_1_result_{gap}.txt'
# # B = folder + f'_random_2_result_{gap}.txt'
from get_total_t_k import get_pro_result,get_random_all,get_random1,get_rand_pro_result

label_list = [4,34,72,107,158]

# AorB = 4
gap = 0.2
data = './figure/dawn/dawn'
# label_name = './original-data/contact-primary-school-classes-gender/node-labels-get.txt'
# edge_name = './original-data/contact-high-school-classes-gender/hyperedges-contact-high-school-classes-gender.txt'
# original-data\contact-high-school-classes-gender\
edge_name = 'DAWN\DAWN-cleaned_hyperedges.txt'
for AorB in label_list:
    result,class_propotion,k_count = get_pro_result(label_file_name=file_name,edge_file_name=edge_name,data_name=data,AorB = AorB,gap=gap)

print("k_count",k_count)
# edge_name = data+ "_random_edge.txt"
# node_name = data + '_random_node.txt'
# get_random_all(k_count,class_propotion,edge_name,node_name)

# AorB = 4
# gap = 0.05
data_name = data+'_random'
for AorB in label_list:
    result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = data_name,AorB = AorB,gap=gap)

    # result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = data_name,AorB = AorB,gap=gap)
# AorB = 34
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)
# AorB = 72
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)
# AorB = 107
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)
# AorB = 158
# result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name=data_name,AorB = AorB,gap=gap)

print(class_propotion)
print(k_count)
print(class_propotion)
print(k_count)
# m = 0
# k = []
# for i in k_count:
#     m+=i[1]
#     k.append(i[0])
# # print(max(k))
# print(m)
# print(class_propotion[1]+class_propotion[2])

# from plt_for_all import get_result,plt_all2
# # # gap = 0.1
# # k_max = k_count[-1][0]
# # print(k_max)
# k_max = 15
# folder = data
# # # 这里改aorb
# gap = 0.2
# origin_A = folder +f'_{label_list[0]}_result_{gap}.txt'
# origin_B = folder +f'_{label_list[1]}_result_{gap}.txt'
# origin_C = folder +f'_{label_list[2]}_result_{gap}.txt'
# origin_D = folder +f'_{label_list[3]}_result_{gap}.txt'
# origin_E = folder +f'_{label_list[4]}_result_{gap}.txt'


# A = folder + f'_random_{label_list[0]}_result_{gap}.txt'
# B = folder + f'_random_{label_list[1]}_result_{gap}.txt'
# C = folder + f'_random_{label_list[2]}_result_{gap}.txt'
# D = folder + f'_random_{label_list[3]}_result_{gap}.txt'
# E = folder + f'_random_{label_list[4]}_result_{gap}.txt'

# result_origin_A = get_result(origin_A)
# result_origin_B = get_result(origin_B)
# result_origin_C = get_result(origin_C)
# result_origin_D = get_result(origin_D)
# result_origin_E = get_result(origin_E)
# result_A = get_result(A)
# result_B = get_result(B)
# result_C = get_result(C)
# result_D = get_result(D)
# result_E = get_result(E)
# # plt_all1(result_A,result_B,result_C,result_origin_A,result_origin_B,result_origin_C,gap,k_max,label=['Food, Household & Pets',"Pharmacy, Health & Beauty","Clothing, Shoes & Accessories"],folder=folder,symmet=False)
# # plt_all2(result_A,result_B,result_C,result_D,result_E,result_origin_A,result_origin_B,result_origin_C,result_origin_D,result_origin_E,gap,k_max,label=["4","34","32","107","158"],folder=folder,symmet=False)


