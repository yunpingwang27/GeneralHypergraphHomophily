

# # # 目前是这样，我想借用BRHM的模型，这样的话，应该怎么改呢？
# # # 但是事实上，BRHM的模型是从m个特定k-tuple中随机选特定的数量，生成超边，我怎么体现出同质性，就是同类的节点占比较多的tuple更容易形成超边呢？


# # # 2,3,4,5
# # # 500,800，600,400

# # # A = 500
# # # B = 500

# # # baseline 随机从A+B中选k个节点,生成超边

# # # 比如k = 5, 从A中选4个，从B中选1个，生成超边的概率是C(500,4)*C(500,1)/C(1000,5)

# # # 但是如果我们想体现同质性，我们可以拿 h(e) =  同类节点对数量/总节点对数量
# # # 比方说5个节点的tuple中，4个来自A，1个来自B，那么同类节点对数量是C(4,2)/C(5,2) = 6/10 = 0.6
# # # 也可以用熵来表示，比如5个节点的tuple中，4个来自A，1个来自B，那么熵是 - (4/5 * log(4/5) + 1/5 * log(1/5)) = 0.72，同质性越高，熵越低
# # # 表现出我们以更大的概率选取同质性更高的tuple来生成超边，

# import numpy as np
# from math import comb
# from collections import Counter


# import numpy as np
# from math import comb

# import numpy as np
# from math import comb

# def homogeneity_from_counts(a, b, alpha=2):
#     """同类节点对比例（同质性）"""
#     k = a + b
#     if k < 2:
#         return 1.0
#     # same_pairs = comb(a, 2) + comb(b, 2)
#     # total_pairs = comb(k, 2)
#     # return same_pairs / total_pairs
#     return (max(a/(a+b), 0.5))**alpha  # 直接用多数类占比作为同质性得分
# def generate_hyperedges_exact(
#     nA, nB,
#     k_values,
#     num_edges_per_k,
#     epsilon=0.00,      # 👈 新增：低同质性保底因子
#     seed=42,
#     alpha = 2
# ):
#     """
#     超边生成概率 ∝ (同质性 + epsilon) × C(nA,a)×C(nB,b)
#     epsilon > 0 确保同质性为0的组合也有正概率
#     """
#     np.random.seed(seed)
#     A_ids = np.arange(nA)
#     B_ids = np.arange(nA, nA + nB)

#     hyperedges = {}
#     stats = {}

#     for k, n_edges in zip(k_values, num_edges_per_k):
#         # 枚举所有可行的 (a,b)
#         a_min = max(0, k - nB)
#         a_max = min(k, nA)
#         a_vals, b_vals, weights = [], [], []
#         for a in range(a_min, a_max + 1):
#             b = k - a
#             homo = homogeneity_from_counts(a, b,alpha=alpha)
#             comb_total = comb(nA, a) * comb(nB, b)
#             # 🟢 关键修改：加上 epsilon，保证权重 > 0
#             w = (homo + epsilon) * comb_total
#             a_vals.append(a)
#             b_vals.append(b)
#             weights.append(w)

#         # 归一化
#         weights = np.array(weights, dtype=float)
#         probs = weights / weights.sum() if weights.sum() > 0 else np.ones_like(weights) / len(weights)

#         # 生成超边
#         edges_k = []
#         homo_scores = []
#         for _ in range(n_edges):
#             idx = np.random.choice(len(a_vals), p=probs)
#             a = a_vals[idx]
#             b = b_vals[idx]
#             chosen_A = np.random.choice(A_ids, size=a, replace=False) if a > 0 else []
#             chosen_B = np.random.choice(B_ids, size=b, replace=False) if b > 0 else []
#             edge = tuple(np.concatenate([chosen_A, chosen_B]))
#             edges_k.append(edge)
#             homo_scores.append(homogeneity_from_counts(a, b,alpha=alpha))

#         hyperedges[k] = edges_k
#         stats[k] = {
#             'avg_homogeneity': np.mean(homo_scores),
#             'std': np.std(homo_scores),
#             'min': np.min(homo_scores),
#             'max': np.max(homo_scores),
#             'class_probs': dict(zip([(a,b) for a,b in zip(a_vals,b_vals)], probs)),
#             'epsilon': epsilon   # 记录使用的 epsilon
#         }

#     return hyperedges, stats
# # # ---------- 精确概率采样（基于所有可能k元组） ----------
# # def generate_hyperedges_exact(
# #     nA, nB,
# #     k_values,
# #     num_edges_per_k,
# #     seed=42
# # ):
# #     """
# #     超边生成概率 ∝ 同质性得分 × C(nA,a)×C(nB,b)
# #     参数：
# #         nA, nB : 两类节点数量
# #         k_values : 超边大小列表
# #         num_edges_per_k : 每种大小要生成的超边数量
# #     返回：
# #         hyperedges : dict {k: [edge_tuple, ...]}
# #         stats : dict {k: {'avg_homogeneity':..., ...}}
# #     """
# #     np.random.seed(seed)
# #     # 节点ID分配：0..nA-1为A类，nA..nA+nB-1为B类
# #     A_ids = np.arange(nA)
# #     B_ids = np.arange(nA, nA + nB)
    
# #     hyperedges = {}
# #     stats = {}
    
# #     for k, n_edges in zip(k_values, num_edges_per_k):
# #         # ---- 1. 枚举所有可能的(a,b)组合 ----
# #         a_min = max(0, k - nB)
# #         a_max = min(k, nA)
# #         a_vals = []
# #         b_vals = []
# #         weights = []
# #         comb_counts = []   # 记录组合数，仅用于后续打印（非必须）
        
# #         for a in range(a_min, a_max + 1):
# #             b = k - a
# #             # 同质性得分（同类节点对比例）
# #             homo = homogeneity_from_counts(a, b)
# #             # 实际组合数
# #             comb_a = comb(nA, a)
# #             comb_b = comb(nB, b)
# #             comb_total = comb_a * comb_b
# #             # 权重 = 同质性 × 组合数
# #             w = homo * comb_total
# #             a_vals.append(a)
# #             b_vals.append(b)
# #             weights.append(w)
# #             comb_counts.append(comb_total)
        
# #         # ---- 2. 归一化得到各类别采样概率 ----
# #         weights = np.array(weights, dtype=float)
# #         if weights.sum() == 0:
# #             probs = np.ones_like(weights) / len(weights)
# #         else:
# #             probs = weights / weights.sum()
        
# #         # ---- 3. 按概率生成指定数量的超边 ----
# #         edges_k = []
# #         for _ in range(n_edges):
# #             # 根据概率选择一个类别构成
# #             idx = np.random.choice(len(a_vals), p=probs)
# #             a = a_vals[idx]
# #             b = b_vals[idx]
# #             # 从对应类别中随机抽取节点（不重复）
# #             chosen_A = np.random.choice(A_ids, size=a, replace=False) if a > 0 else []
# #             chosen_B = np.random.choice(B_ids, size=b, replace=False) if b > 0 else []
# #             edge = tuple(np.concatenate([chosen_A, chosen_B]))
# #             # 随机打乱节点顺序（超边是无序集合，但通常存储为元组，顺序不重要）
# #             # 这里保持原顺序也可，为统计同质性时需根据标签计算，不影响结果
# #             edges_k.append(edge)
        
# #         hyperedges[k] = edges_k
        
# #         # ---- 4. 统计实际生成超边的同质性 ----
# #         # 为统计需要，重新获取每个超边的标签（也可直接由a,b推断，但这里重新计算）
# #         labels_all = np.array([0]*nA + [1]*nB)
# #         homo_scores = []
# #         for e in edges_k:
# #             node_labels = labels_all[list(e)]
# #             cls_counts = np.bincount(node_labels)
# #             # 重新计算同类节点对比例（与homogeneity_from_counts等价）
# #             if len(e) >= 2:
# #                 same = sum(comb(c,2) for c in cls_counts)
# #                 total = comb(len(e),2)
# #                 homo_scores.append(same/total)
# #             else:
# #                 homo_scores.append(1.0)
        
# #         stats[k] = {
# #             'avg_homogeneity': np.mean(homo_scores),
# #             'std': np.std(homo_scores),
# #             'min': np.min(homo_scores),
# #             'max': np.max(homo_scores),
# #             # 以下为各类别的理论概率（可选项）
# #             'class_probs': dict(zip([(a,b) for a,b in zip(a_vals,b_vals)], probs))
# #         }
    
# #     return hyperedges, stats

# # ---------- 均匀随机生成（基线，保持不变） ----------
# def generate_hyperedges_uniform(nA, nB, k_values, num_edges_per_k, seed=42):
#     np.random.seed(seed)
#     node_ids = np.arange(nA + nB)
#     labels = np.array([0]*nA + [1]*nB)
#     hyperedges = {}
#     stats = {}
#     for k, n_edges in zip(k_values, num_edges_per_k):
#         edges = []
#         for _ in range(n_edges):
#             edge = tuple(np.random.choice(node_ids, size=k, replace=False))
#             edges.append(edge)
#         hyperedges[k] = edges
#         homo_scores = []
#         for e in edges:
#             node_labels = labels[list(e)]
#             cls_counts = np.bincount(node_labels)
#             if len(e) >= 2:
#                 same = sum(comb(c,2) for c in cls_counts)
#                 total = comb(len(e),2)
#                 homo_scores.append(same/total)
#             else:
#                 homo_scores.append(1.0)
#         stats[k] = {
#             'avg_homogeneity': np.mean(homo_scores),
#             'std': np.std(homo_scores)
#         }
#     return hyperedges, stats

# from get_random_kl_divergence import get_summary
# # from random_hyper_pro import 
# # ---------- 示例：A=500, B=500，生成2,3,4,5阶超边 ----------
# if __name__ == '__main__':
#     nA, nB = 600, 600
#     k_max = 25
#     if k_max <=9:
#         gap = 0.2
#     elif k_max <= 19:
#         gap = 0.1
#     elif k_max <= 40:
#         gap = 0.05
#     elif k_max <= 50:
#         gap =0.025
#     alpha = 0
#     k_vals = [i for i in range(2,k_max+1)]
#     pro_edge_per_k = [k**(-2.5) for k in k_vals]
#     pro_sum = np.sum(pro_edge_per_k)
#     n_edges_per_k = [int(pro_k/pro_sum*10000) for pro_k in pro_edge_per_k]

#     # n_edges_per_k = [500,1000, 800, 700,500,400,300,300,300]
    
#     print("=== 同质性偏好生成（精确概率 ∝ 同质性×组合数） ===")
#     homo_edges, homo_stats = generate_hyperedges_exact(
#         nA, nB, k_vals, n_edges_per_k, seed=123,alpha=alpha
#     )
#     # print(homo_edges)
#     for k in k_vals:
#         print(f"k={k}: 平均同质性 = {homo_stats[k]['avg_homogeneity']:.4f} "
#               f"(理论范围: {homo_stats[k]['min']:.4f}~{homo_stats[k]['max']:.4f})")
    
#     print("\n=== 均匀随机生成（基线） ===")
#     uniform_edges, uniform_stats = generate_hyperedges_uniform(
#         nA, nB, k_vals, n_edges_per_k, seed=123
#     )
#     for k in k_vals:
#         print(f"k={k}: 平均同质性 = {uniform_stats[k]['avg_homogeneity']:.4f}")
#     # 保存同质性生成的超边
#     with open('./random_kl/node_label.txt', 'w') as f:
#         for i in range(nA):
#             f.write('1\n')
#         for i in range(nB):
#             f.write('2\n')
#     with open('./random_kl/homo_edges.txt', 'w') as f:
#         for k, edge_list in homo_edges.items():   # 遍历每个阶
#             for edge in edge_list:                # 遍历该阶的每个超边
#                 f.write(','.join(map(str,map(int, edge))) + '\n')
#     with open('./random_kl/uniform_edges.txt', 'w') as f:
#         for k, edge_list in uniform_edges.items():   # 遍历每个阶
#             for edge in edge_list:                # 遍历该阶的每个超边
#                 f.write(','.join(map(str,map(int, edge))) + '\n')
#     from get_total_t_k import get_pro_result, get_random, get_rand_pro_result
#     AorB = 1
#     folder ="./random_kl/"
#     data = folder+'homophily'
#     result,class_propotion,k_count = get_pro_result(label_file_name='random_kl/node_label.txt',edge_file_name='random_kl/homo_edges.txt',data_name=data,AorB = AorB,gap=gap)
#     # print(k_count)
#     # print(result)
#     AorB = 2
#     # gap = 0.1
#     result,class_propotion,k_count = get_pro_result(label_file_name='random_kl/node_label.txt',edge_file_name='random_kl/homo_edges.txt',data_name=data ,AorB = AorB,gap=gap)

#     # print(result)
#     edge_name = data+ "_random_edge.txt"
#     node_name = data + '_random_node.txt'
#     # get_random(k_count,class_propotion,edge_name,node_name)
#     AorB = 1
#     dataname = data + "_random"
#     # gap = 0.1
#     # result,class_propotion,k_count = get_pro_result(label_file_name=node_name,edge_file_name=edge_name,data_name = dataname,AorB = AorB,gap=gap)
#     result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = dataname,AorB = AorB,gap=gap)

#     AorB = 2
#     result,class_propotion,k_count = get_rand_pro_result(k_count,class_propotion,data_name = dataname,AorB = AorB,gap=gap)

#     folder = './random_kl/'
#     class_list = [1,2]

#     data_pre = "homophily"
#     # gap = 0.2
#     kl = get_summary(folder,data_pre,gap,class_list)


import numpy as np
from math import comb
import matplotlib.pyplot as plt
from get_total_t_k import get_pro_result, get_random, get_rand_pro_result
from get_random_kl_divergence import get_summary

def homogeneity_from_counts(a, b, alpha=2):
    """同质性得分 = (多数类比例)^α"""
    k = a + b
    if k == 0:
        return 1.0
    return (max(a/k, 0.5))**alpha

def generate_hyperedges_exact(
    nA, nB,
    k_values,
    num_edges_per_k,
    epsilon=0.01,      # 保底概率，避免零权重
    seed=42,
    alpha=2
):
    """按权重 ∝ (同质性+ε)×C(nA,a)×C(nB,b) 生成超边"""
    np.random.seed(seed)
    A_ids = np.arange(nA)
    B_ids = np.arange(nA, nA + nB)

    hyperedges = {}
    stats = {}

    for k, n_edges in zip(k_values, num_edges_per_k):
        a_min = max(0, k - nB)
        a_max = min(k, nA)
        a_vals, b_vals, weights = [], [], []
        for a in range(a_min, a_max + 1):
            b = k - a
            homo = homogeneity_from_counts(a, b, alpha=alpha)
            comb_total = comb(nA, a) * comb(nB, b)
            w = (homo + epsilon) * comb_total
            a_vals.append(a)
            b_vals.append(b)
            weights.append(w)

        weights = np.array(weights, dtype=float)
        probs = weights / weights.sum() if weights.sum() > 0 else np.ones_like(weights) / len(weights)

        edges_k = []
        homo_scores = []
        for _ in range(n_edges):
            idx = np.random.choice(len(a_vals), p=probs)
            a = a_vals[idx]
            b = b_vals[idx]
            chosen_A = np.random.choice(A_ids, size=a, replace=False) if a > 0 else []
            chosen_B = np.random.choice(B_ids, size=b, replace=False) if b > 0 else []
            edge = tuple(np.concatenate([chosen_A, chosen_B]))
            edges_k.append(edge)
            homo_scores.append(homogeneity_from_counts(a, b, alpha=alpha))

        hyperedges[k] = edges_k
        stats[k] = {
            'avg_homogeneity': np.mean(homo_scores),
            'std': np.std(homo_scores),
            'min': np.min(homo_scores),
            'max': np.max(homo_scores),
            'class_probs': dict(zip([(a,b) for a,b in zip(a_vals,b_vals)], probs)),
            'epsilon': epsilon
        }

    return hyperedges, stats

if __name__ == '__main__':
    # ---------- 固定参数 ----------
    nA, nB = 600, 600          # 两类节点各600
    k_max = 25                 # 最大超边大小
    # 根据k_max确定gap（用于统计分组）
    if k_max <= 9:
        gap = 0.2
    elif k_max <= 19:
        gap = 0.1
    elif k_max <= 40:
        gap = 0.05
    elif k_max <= 50:
        gap = 0.025
    else:
        gap = 0.02

    # 超边大小分布（幂律）
    k_vals = list(range(2, k_max + 1))
    pro_edge_per_k = [k ** (-2.5) for k in k_vals]
    pro_sum = np.sum(pro_edge_per_k)
    n_edges_per_k = [int(pro_k / pro_sum * 10000) for pro_k in pro_edge_per_k]

    folder = "./random_kl/"   # 工作目录
    class_list = [1, 2]       # 节点类别标签
    epsilon = 0.01            # 保底因子，确保所有组合非零概率

    # ---------- 生成节点标签文件（固定）----------
    with open(folder + 'node_label.txt', 'w') as f:
        for _ in range(nA):
            f.write('1\n')
        for _ in range(nB):
            f.write('2\n')
    # k_max = 25
    k_maxs = list(range(5, 25 + 1))
    # ---------- 遍历α ----------
    # alpha_values = np.arange(0, 3.1, 0.5)   # 0.0, 0.2, ..., 3.0
    k_ma_item, kls = [], []

    for k_max in k_maxs:
        if k_max <= 10:
            gap = 0.2
        elif k_max <= 19:
            gap = 0.1
        elif k_max <= 40:
            gap = 0.05
        elif k_max <= 50:
            gap = 0.025
        else:
            gap = 0.02
        # gap = 0.02
        alpha = 2
        k_vals = list(range(2, k_max + 1))
        pro_edge_per_k = [k ** (-2.5) for k in k_vals]
        pro_sum = np.sum(pro_edge_per_k)
        n_edges_per_k = [int(pro_k / pro_sum * 10000) for pro_k in pro_edge_per_k]

        print(f"\n========== α = {k_max:.2f} ==========")
        suffix = f"_alpha{k_max:.2f}"
        data_pre = f"homophily{suffix}"           # 数据名前缀（不带路径）
        edge_file = f"homo_edges{suffix}.txt"     # 超边文件名

        # 1. 生成同质性超边
        homo_edges, _ = generate_hyperedges_exact(
            nA, nB, k_vals, n_edges_per_k,
            epsilon=epsilon, seed=123, alpha=alpha
        )

        # 保存超边文件
        with open(folder + edge_file, 'w') as f:
            for k, edge_list in homo_edges.items():
                for edge in edge_list:
                    f.write(','.join(map(str, map(int, edge))) + '\n')

        # 2. 计算真实超图的统计量（分别考察类别1和类别2）
        data = folder + data_pre   # 完整前缀（含路径）
        # 类别1
        result1, class_propotion1, k_count1 = get_pro_result(
            label_file_name=folder + 'node_label.txt',
            edge_file_name=folder + edge_file,
            data_name=data,
            AorB=1,
            gap=gap
        )
        # 类别2
        result2, class_propotion2, k_count2 = get_pro_result(
            label_file_name=folder + 'node_label.txt',
            edge_file_name=folder + edge_file,
            data_name=data,
            AorB=2,
            gap=gap
        )

        # 3. 生成配置模型随机零假设超边（基于类别1的统计）
        class_propotion = class_propotion1
        k_count = k_count1
        rand_edge_name = folder + data_pre + "_random_edge.txt"
        rand_node_name = folder + data_pre + "_random_node.txt"
        get_random(k_count, class_propotion, rand_edge_name, rand_node_name)

        # 4. 计算随机零假设的统计量
        dataname = data + "_random"
        rand_result1, _, _ = get_rand_pro_result(
            k_count, class_propotion, data_name=dataname, AorB=1, gap=gap
        )
        rand_result2, _, _ = get_rand_pro_result(
            k_count, class_propotion, data_name=dataname, AorB=2, gap=gap
        )

        # 5. 计算KL散度
        kl = get_summary(folder, data_pre, gap, class_list)
        print(f"KL divergence = {kl:.6f}")

        k_ma_item.append(k_max)
        kls.append(kl)

    # ---------- 绘制KL–α曲线 ----------
    plt.figure(figsize=(6,4))
    plt.plot(k_ma_item, kls, marker='o', linestyle='-', linewidth=2, markersize=6,color = 'k')
    plt.xlabel(r'$k_{max}$', fontsize=14)
    plt.ylabel('I-Divergence', fontsize=14)
    plt.ylim(0.1,0.25)
    # plt.title(r'KL Divergence vs $\gamma$ (Homophilic Hypergraph Model)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(folder + 'kl_k_curve2.png', dpi=300)