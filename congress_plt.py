from plt_for_all import get_result,plt_all
gap = 0.05
k_max = 25
folder = "./figure/congress/"
result_origin_A = get_result(folder+f'congress_1_result_{gap}.txt')
result_origin_B = get_result(folder+f'congress_2_result_{gap}.txt')
result_A = get_result(folder+f'congress_random_1_result_{gap}.txt')
result_B = get_result(folder+f'congress_random_2_result_{gap}.txt')
plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label=['Democrat','Republican'])

