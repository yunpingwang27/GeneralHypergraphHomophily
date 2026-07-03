
from plt_for_all import get_result,plt_all1
label_list = [4,34,72,107,158]

data = './figure/dawn/dawn'
# k_max = 15
folder = data
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
# plt_all1(result_A,result_B,result_C,result_origin_A,result_origin_B,result_origin_C,gap,k_max,label=['Food, Household & Pets',"Pharmacy, Health & Beauty","Clothing, Shoes & Accessories"],folder=folder,symmet=False)
# plt_all1(result_A,result_B,result_C,result_origin_A,result_origin_B,result_origin_C,gap,k_max,label=["A","B","C"],folder=folder,symmet=False)
# plt_all2()

# result = []
# result_origin = []
# class_num = 4
# for i in range(class_num):
#     origin_A = folder +f'_{label_list[i]}_result_{gap}.txt'
#     A = folder + f'_random_{label_list[i]}_result_{gap}.txt'

#     result_origin.append(get_result(origin_A))
#     result.append(get_result(A))
# plt_all2(result,result_origin,class_num,gap,k_max,label=label_list,folder=folder,symmet=False)


from plt_for_all import get_result,plt_all2
# # gap = 0.1
k_max = 15
gap = 0.2


result = []
result_origin = []
for i in range(5):
    origin_A = folder +f'_{label_list[i]}_result_{gap}.txt'
    A = folder + f'_random_{label_list[i]}_result_{gap}.txt'

    result_origin.append(get_result(origin_A))
    result.append(get_result(A))
plt_all2(result,result_origin,5,gap,k_max,label=label_list,folder=folder,symmet=False)


