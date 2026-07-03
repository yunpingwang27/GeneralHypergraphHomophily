from plt_for_all import get_result,plt_all
gap = 0.1
k_max = 10
folder = "./random_kl/"
result_origin_A = get_result(folder+f'homophily_1_result_{gap}.txt')
result_origin_B = get_result(folder+f'homophily_2_result_{gap}.txt')
result_A = get_result(folder+f'homophily_random_1_result_{gap}.txt')
result_B = get_result(folder+f'homophily_random_2_result_{gap}.txt')
plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label=['A','B'],folder="./random_kl/homophily")

