from plt_for_all import get_result,plt_all
gap = 0.2
k_max = 5
folder = 'figure/primary/primary'
# folder = 'figure/high/high'
origin_A = folder +'_1_result_0.2.txt'
origin_B = folder +'_2_result_0.2.txt'
A = folder + '_random_1_result_0.2.txt'
B = folder + '_random_2_result_0.2.txt'
result_origin_A = get_result(origin_A)
result_origin_B = get_result(origin_B)
result_A = get_result(A)
result_B = get_result(B)
plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label=['Male','Female'],folder=folder)