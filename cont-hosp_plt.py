
folder = './figure/hospital/hospital'
label_list = [0,1,2,3,4]

from plt_for_all import get_result,plt_all2
# # gap = 0.1
k_max = 8
gap = 0.2


result = []
result_origin = []
class_num = 4
for i in range(class_num):
    origin_A = folder +f'_{label_list[i]}_result_{gap}.txt'
    A = folder + f'_random_{label_list[i]}_result_{gap}.txt'

    result_origin.append(get_result(origin_A))
    result.append(get_result(A))
plt_all2(result,result_origin,class_num,gap,k_max,label=label_list,folder=folder,symmet=False)

# class {0: 8, 1: 28, 2: 11, 3: 29, 4: 5}
