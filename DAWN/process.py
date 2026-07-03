# # 简洁版本
# def generate_hyperedges():
#     # 读取数据
#     with open('DAWN/DAWN-nverts.txt', 'r') as f:
#         nverts = [int(line.strip()) for line in f if line.strip()]
    
#     with open('DAWN/DAWN-simplices.txt', 'r') as f:
#         simplices = [int(line.strip()) for line in f if line.strip()]
    
#     # 生成超边
#     current = 0
#     with open('hyperedges.txt', 'w') as f:
#         for n in nverts:
#             edge = simplices[current:current+n]
#             f.write(','.join(map(str, edge)) + '\n')
#             current += n
    
#     print("超边生成完成！")

# # # 运行
# # generate_hyperedges()
# import pandas as pd
# from collections import Counter

# # 数据
# data = pd.read_csv("DAWN\labels.csv",header=0)
# # 统计每个group_code的出现次数
# group_counts = Counter(data['group_code'])

# print("每个group_code的出现次数:")
# for code, count in group_counts.items():
#     print(f"group_code {code}: {count}次")

# print("\n出现次数最多的5个group_code:")
# # 获取出现次数最多的5个
# most_common = group_counts.most_common(5)

# for i, (code, count) in enumerate(most_common, 1):
#     print(f"{i}. group_code {code}: {count}次")

# #     出现次数最多的5个group_code:
# # 2. group_code 4: 54次
# # 1. group_code 34: 159次
# # 3. group_code 72: 47次
# # 4. group_code 107: 46次
# # 5. group_code 158: 46次

def analyze_and_clean_hyperedges(input_file, output_file=None):
    """
    分析并清理超边文件，删除单点超边
    """
    # 读取数据
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print("=== 处理前分析 ===")
    single_node_count = 0
    multi_node_count = 0
    node_distribution = {}
    
    for line in lines:
        nodes = line.split(',')
        node_count = len(nodes)
        
        # 统计节点数量分布
        if node_count in node_distribution:
            node_distribution[node_count] += 1
        else:
            node_distribution[node_count] = 1
        
        # 统计单点和多点超边
        if node_count == 1:
            single_node_count += 1
        else:
            multi_node_count += 1
    
    print(f"总超边数: {len(lines)}")
    print(f"单点超边数: {single_node_count}")
    print(f"多点超边数: {multi_node_count}")
    print("节点数量分布:", dict(sorted(node_distribution.items())))
    
    # 过滤单点超边
    filtered_lines = [line for line in lines if len(line.split(',')) > 1]
    
    print("\n=== 处理后结果 ===")
    print(f"保留超边数: {len(filtered_lines)}")
    print(f"删除超边数: {single_node_count}")
    
    # 确定输出文件
    if output_file is None:
        output_file = input_file
    
    # 写入结果
    with open(output_file, 'w') as f:
        for line in filtered_lines:
            f.write(line + '\n')
    
    print(f"\n结果已保存到: {output_file}")
    
    # 显示被删除的一些例子
    single_node_examples = [line for line in lines if len(line.split(',')) == 1][:5]
    if single_node_examples:
        print(f"\n删除的单点超边示例: {single_node_examples}")

# 使用示例
if __name__ == "__main__":
    input_file = "DAWN\DAWN-hyperedges.txt"  # 替换为您的文件名
    
    # 分析并清理
    # analyze_and_clean_hyperedges(input_file)
    
    # 或者保存到新文件
    analyze_and_clean_hyperedges(input_file, "DAWN\DAWN-cleaned_hyperedges.txt")