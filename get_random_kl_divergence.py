# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from scipy.special import kl_div, rel_entr

def read_distribution_from_file(filename):
    """从txt文件读取分布数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = [float(line.strip()) for line in f.readlines()]
    return np.array(data)

def calculate_kl_divergence(p, q):
    """
    计算KL散度 D_KL(P || Q)
    
    参数:
    p: 分布P
    q: 分布Q
    
    返回:
    kl_divergence: KL散度值
    """
    # 添加小值避免除零和log(0)问题
    epsilon = 1e-12
    p_smooth = p +epsilon 
    q_smooth = q +epsilon
    # 重新归一化
    # p_smooth = p_smooth
    # q_smooth = q_smooth
    
    kl_value = np.sum(q_smooth * np.log(q_smooth / p_smooth)+p_smooth-q_smooth)
    return kl_value

def calculate_js_divergence(p, q):
    """
    计算JS散度 (Jensen-Shannon Divergence)
    JS散度是对称的，取值范围在[0, 1]之间
    """
    epsilon = 1e-10
    p_smooth = p + epsilon
    q_smooth = q + epsilon
    p_smooth = p_smooth / p_smooth.sum()
    q_smooth = q_smooth / q_smooth.sum()
    
    m = 0.5 * (p_smooth + q_smooth)
    js_value = 0.5 * np.sum(p_smooth * np.log(p_smooth / m)) + 0.5 * np.sum(q_smooth * np.log(q_smooth / m))
    return js_value

def calculate_wasserstein_distance(p, q):
    """
    计算Wasserstein距离（Earth Mover's Distance）
    对于一维分布，可以通过累积分布的差异来计算
    """
    # 计算累积分布
    p_cumulative = np.cumsum(p)
    q_cumulative = np.cumsum(q)
    
    # Wasserstein距离是累积分布差异的积分
    wasserstein = np.sum(np.abs(p_cumulative - q_cumulative))
    return wasserstein

def analyze_distribution_differences_enhanced(test_data, baseline_data, output_prefix="distribution_analysis"):
    """
    增强版的分布差异分析，包含信息论距离度量
    """
    
    # 确保两个分布长度相同
    if len(test_data) != len(baseline_data):
        min_len = min(len(test_data), len(baseline_data))
        test_data = test_data[:min_len]
        baseline_data = baseline_data[:min_len]
        print(f"警告: 分布长度不同，截取前{min_len}个数据点")
    
    n_bins = len(test_data)
    
    print("=" * 60)
    print("分布差异分析报告（增强版）")
    print("=" * 60)
    
    # 1. 基本统计信息
    print("\n1. 基本统计信息:")
    print(f"数据点数: {n_bins}")
    print(f"测试数据总和: {test_data.sum():.6f}")
    print(f"基线数据总和: {baseline_data.sum():.6f}")
    
    # 2. 信息论距离度量
    print("\n2. 信息论距离度量:")
    
    # KL散度 (不对称)
    kl_pq = calculate_kl_divergence(test_data, baseline_data)
    kl_qp = calculate_kl_divergence(baseline_data, test_data)
    print(f"KL散度 D_KL(测试||基线): {kl_pq:.6f}")
    print(f"KL散度 D_KL(基线||测试): {kl_qp:.6f}")
    print(f"对称KL散度: {0.5 * (kl_pq + kl_qp):.6f}")
    
    # JS散度 (对称)
    js_div = calculate_js_divergence(test_data, baseline_data)
    print(f"JS散度: {js_div:.6f}")
    
    # Wasserstein距离
    wasserstein = calculate_wasserstein_distance(test_data, baseline_data)
    print(f"Wasserstein距离: {wasserstein:.6f}")
    
    # 3. 传统统计差异
    differences = test_data - baseline_data
    absolute_diff = np.abs(differences)
    
    print("\n3. 传统差异统计:")
    print(f"平均绝对差异: {absolute_diff.mean():.6f}")
    print(f"最大绝对差异: {absolute_diff.max():.6f}")
    print(f"差异标准差: {differences.std():.6f}")
    
    # 4. 统计检验
    print("\n4. 统计检验:")
    ks_stat, ks_pvalue = stats.ks_2samp(test_data, baseline_data)
    print(f"KS检验统计量: {ks_stat:.6f}")
    print(f"KS检验p值: {ks_pvalue:.6f}")
    
    # 5. 相关性分析
    correlation = np.corrcoef(test_data, baseline_data)[0, 1]
    print(f"\n5. 相关性分析:")
    print(f"皮尔逊相关系数: {correlation:.6f}")
    
    # 6. 解释KL散度值的意义
    print(f"\n6. KL散度解释:")
    interpret_kl_divergence(kl_pq)
    
    # 保存结果
    save_enhanced_results(test_data, baseline_data, differences, kl_pq, kl_qp, js_div, wasserstein, output_prefix)
    
    return {
        'kl_divergence_pq': kl_pq,
        'kl_divergence_qp': kl_qp,
        'js_divergence': js_div,
        'wasserstein_distance': wasserstein,
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pvalue,
        'correlation': correlation,
        'mean_absolute_difference': absolute_diff.mean()
    }

def interpret_kl_divergence(kl_value):
    """解释KL散度值的意义"""
    if kl_value < 0.01:
        print("  KL散度 < 0.01: 分布非常相似")
    elif kl_value < 0.05:
        print("  KL散度 0.01-0.05: 分布比较相似")
    elif kl_value < 0.1:
        print("  KL散度 0.05-0.1: 分布有可察觉的差异")
    elif kl_value < 0.5:
        print("  KL散度 0.1-0.5: 分布有明显差异")
    else:
        print("  KL散度 > 0.5: 分布差异很大")

def save_enhanced_results(test_data, baseline_data, differences, kl_pq, kl_qp, js_div, wasserstein, output_prefix):
    """保存增强的分析结果到文件"""
    
    # 保存详细数据
    with open(f'{output_prefix}_detailed_results.txt', 'w', encoding='utf-8') as f:
        f.write("区间索引\t测试分布\t基线分布\t差异\tlog(P/Q)\tKL贡献\n")
        epsilon = 1e-10
        for i in range(len(test_data)):
            p = test_data[i] + epsilon
            q = baseline_data[i] + epsilon
            log_ratio = np.log(p / q)
            kl_contribution = test_data[i] * log_ratio if test_data[i] > 0 else 0
            f.write(f"{i}\t{test_data[i]:.6f}\t{baseline_data[i]:.6f}\t{differences[i]:.6f}\t{log_ratio:.6f}\t{kl_contribution:.6f}\n")
    
    # 保存摘要统计
    with open(f'{output_prefix}_summary.txt', 'w', encoding='utf-8') as f:
        f.write("分布差异分析摘要（增强版）\n")
        f.write("=" * 40 + "\n")
        f.write(f"数据点数: {len(test_data)}\n\n")
        
        f.write("信息论距离度量:\n")
        f.write(f"KL散度 D_KL(测试||基线): {kl_pq:.6f}\n")
        f.write(f"KL散度 D_KL(基线||测试): {kl_qp:.6f}\n")
        f.write(f"对称KL散度: {0.5 * (kl_pq + kl_qp):.6f}\n")
        f.write(f"JS散度: {js_div:.6f}\n")
        f.write(f"Wasserstein距离: {wasserstein:.6f}\n\n")
        
        f.write("传统统计量:\n")
        f.write(f"平均绝对差异: {np.abs(differences).mean():.6f}\n")
        f.write(f"最大绝对差异: {np.abs(differences).max():.6f}\n")
        f.write(f"差异标准差: {differences.std():.6f}\n")
        f.write(f"皮尔逊相关系数: {np.corrcoef(test_data, baseline_data)[0,1]:.6f}\n")

def get_summary(folder,data_pre,gap,class_list):
    # folder = "./figure/dblp/"
    # data_pre = "dblp"
    # gap = 0.1

    for label in class_list:
    # label = 2
        test_distribution = read_distribution_from_file(folder+data_pre+f"_{label}_result_{gap}.txt")
        
        # 读取基线数据
        baseline_distribution = read_distribution_from_file(folder+data_pre+f"_random_{label}_result_{gap}.txt")
        
        # 进行增强分析
        results = analyze_distribution_differences_enhanced(test_distribution, baseline_distribution,"./diff/"+data_pre+f"_{label}")
        
        print("\n分析完成！")
        print("生成的文件:")
        print("- enhanced_analysis_detailed_results.txt: 详细数据（包含KL贡献）")
        print("- enhanced_analysis_summary.txt: 摘要统计")
        return results["kl_divergence_pq"]
# 使用示例
if __name__ == "__main__":
    # 读取你的数据
    folder = './random_kl/'
    class_list = [1,2]

    data_pre = "homophily"
    gap = 0.2
    get_summary(folder,data_pre,gap,class_list)





  