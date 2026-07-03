
from plt_for_all import get_result,plt_all1
gap = 0.1
# k_max = k_count[-1][0]
# print(k_max)
k_max = 25
# folder = data
data = './figure/walmart/walmart'

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

