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
    epsilon=0.01,
    seed=42,
    alpha=2
):
    """按权重 ∝ (同质性+ε)×C(nA,a)×C(nB,b) 生成超边（支持多 k 值）"""
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

# ========== 新增：生成单一 k 的超边 ==========
def generate_hyperedges_single_k(
    nA, nB,
    k,
    num_edges,
    epsilon=0.01,
    seed=42,
    alpha=2
):
    """生成所有大小均为 k 的超边（固定边数 num_edges）"""
    np.random.seed(seed)
    A_ids = np.arange(nA)
    B_ids = np.arange(nA, nA + nB)

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

    edges = []
    for _ in range(num_edges):
        idx = np.random.choice(len(a_vals), p=probs)
        a = a_vals[idx]
        b = b_vals[idx]
        chosen_A = np.random.choice(A_ids, size=a, replace=False) if a > 0 else []
        chosen_B = np.random.choice(B_ids, size=b, replace=False) if b > 0 else []
        edge = np.concatenate([chosen_A, chosen_B])
        edges.append(edge)

    return edges

if __name__ == '__main__':
    # ---------- 固定参数 ----------
    nA, nB = 600, 600
    k_max = 25
    # 根据k_max确定gap（用于统计分组）
    # if k_max <= 9:
    #     gap = 0.2
    # elif k_max <= 19:
    #     gap = 0.1
    # elif k_max <= 40:
    #     gap = 0.05
    # elif k_max <= 50:
    #     gap = 0.025
    # else:
    #     gap = 0.02
    gap = 0.02

    # 超边大小分布（幂律）
    k_vals = list(range(2, k_max + 1))
    pro_edge_per_k = [k ** (-2.5) for k in k_vals]
    pro_sum = np.sum(pro_edge_per_k)
    n_edges_per_k = [int(pro_k / pro_sum * 10000) for pro_k in pro_edge_per_k]

    folder = "./random_kl/"
    class_list = [1, 2]
    epsilon = 0.01

    # ---------- 生成节点标签文件（固定）----------
    with open(folder + 'node_label.txt', 'w') as f:
        for _ in range(nA):
            f.write('1\n')
        for _ in range(nB):
            f.write('2\n')

    # ========== 第一部分：KL–γ 曲线 ==========
    alpha_values = np.arange(0, 3.1, 0.5)   # γ 取值 0.0, 0.5, ..., 3.0
    alphas, kls = [], []

    for alpha in alpha_values:
        print(f"\n========== α = {alpha:.2f} ==========")
        suffix = f"_alpha{alpha:.2f}"
        data_pre = f"homophily{suffix}"
        edge_file = f"homo_edges{suffix}.txt"

        # 生成同质性超边
        homo_edges, _ = generate_hyperedges_exact(
            nA, nB, k_vals, n_edges_per_k,
            epsilon=epsilon, seed=123, alpha=alpha
        )

        # 保存超边文件
        with open(folder + edge_file, 'w') as f:
            for k, edge_list in homo_edges.items():
                for edge in edge_list:
                    f.write(','.join(map(str, map(int, edge))) + '\n')

        # 计算真实超图统计量
        data = folder + data_pre
        result1, class_propotion1, k_count1 = get_pro_result(
            label_file_name=folder + 'node_label.txt',
            edge_file_name=folder + edge_file,
            data_name=data,
            AorB=1,
            gap=gap
        )
        result2, class_propotion2, k_count2 = get_pro_result(
            label_file_name=folder + 'node_label.txt',
            edge_file_name=folder + edge_file,
            data_name=data,
            AorB=2,
            gap=gap
        )

        # 生成配置模型随机零假设超边（基于类别1的统计）
        class_propotion = class_propotion1
        k_count = k_count1
        rand_edge_name = folder + data_pre + "_random_edge.txt"
        rand_node_name = folder + data_pre + "_random_node.txt"
        get_random(k_count, class_propotion, rand_edge_name, rand_node_name)

        # 计算随机零假设的统计量
        dataname = data + "_random"
        rand_result1, _, _ = get_rand_pro_result(
            k_count, class_propotion, data_name=dataname, AorB=1, gap=gap
        )
        rand_result2, _, _ = get_rand_pro_result(
            k_count, class_propotion, data_name=dataname, AorB=2, gap=gap
        )

        # 计算KL散度
        kl = get_summary(folder, data_pre, gap, class_list)
        print(f"KL divergence = {kl:.6f}")

        alphas.append(alpha)
        kls.append(kl)

    # 绘制KL–γ曲线
    plt.figure(figsize=(6,4))
    plt.plot(alphas, kls, marker='o', linestyle='-', linewidth=2, markersize=6,color = 'k')
    plt.xlabel(r'$\gamma$', fontsize=14)
    plt.ylabel('I-Divergence', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(folder + 'kl_gamma_curve.png', dpi=300)
    plt.close()

    # ========== 新增第二部分：KL–k 曲线（固定 γ=2）==========
    gamma_fixed = 2
    # k_max = 
    k_range = range(5, k_max + 1)           # k = 2..25
    num_edges_per_k_fixed = 1000            # 每个 k 生成 1000 条超边
    kl_k_values = []                        # 存储每个 k 对应的 KL

    print("\n========== 绘制 KL–k 曲线 (γ=2) ==========")
    for k in k_range:
            # 1. 根据当前 k_max 动态计算 gap
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


        print(f"Processing k = {k}")
        suffix = f"_k{k}_gamma{gamma_fixed:.1f}"
        data_pre = f"homophily_k{suffix}"
        edge_file = f"homo_edges{suffix}.txt"

        # 生成所有大小为 k 的超边
        edges = generate_hyperedges_single_k(
            nA, nB, k, num_edges_per_k_fixed,
            epsilon=epsilon, seed=123, alpha=gamma_fixed
        )

        # 保存超边文件
        with open(folder + edge_file, 'w') as f:
            for edge in edges:
                f.write(','.join(map(str, map(int, edge))) + '\n')

        # 计算真实超图统计量（只需类别1）
        data = folder + data_pre
        result1, class_propotion1, k_count1 = get_pro_result(
            label_file_name=folder + 'node_label.txt',
            edge_file_name=folder + edge_file,
            data_name=data,
            AorB=1,
            gap=gap
        )

        # 生成配置模型随机零假设超边（基于类别1的统计）
        class_propotion = class_propotion1
        k_count = k_count1
        rand_edge_name = folder + data_pre + "_random_edge.txt"
        rand_node_name = folder + data_pre + "_random_node.txt"
        get_random(k_count, class_propotion, rand_edge_name, rand_node_name)

        # 计算随机零假设的统计量
        dataname = data + "_random"
        rand_result1, _, _ = get_rand_pro_result(
            k_count, class_propotion, data_name=dataname, AorB=1, gap=gap
        )

        # 计算KL散度
        kl = get_summary(folder, data_pre, gap, class_list)
        print(f"KL divergence for k={k}: {kl:.6f}")
        kl_k_values.append(kl)

    # 绘制KL–k曲线
    plt.figure(figsize=(6,4))
    plt.plot(list(k_range), kl_k_values, marker='s', linestyle='-', linewidth=2, markersize=6)
    plt.xlabel(r'$k$ (hyperedges size)', fontsize=14)
    plt.ylabel('I-Divergence', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(folder + 'kl_k_curve_gamma2.png', dpi=300)
    plt.close()