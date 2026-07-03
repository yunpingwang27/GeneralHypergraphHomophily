from plt_for_all import get_result,plt_all
gap = 0.05
k_max = 21
data = './figure/trip/trip'
# k_max = k_count[-1][0]
folder = data
origin_A = folder +f'_1_result_{gap}.txt'
origin_B = folder +f'_2_result_{gap}.txt'
A = folder + f'_random_1_result_{gap}.txt'
B = folder + f'_random_2_result_{gap}.txt'
result_origin_A = get_result(origin_A)
result_origin_B = get_result(origin_B)
result_A = get_result(A)
result_B = get_result(B)
plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label=['North America','Europe'],folder=folder)

