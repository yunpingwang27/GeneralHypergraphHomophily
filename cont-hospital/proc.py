# import pandas as pd
# import glob
# import os

# def combine_hyperedge_files(output_file='cont-hospital/combined_hyperedges.txt'):
#     """
#     将size-*.csv文件拼接成一个txt文件
    
#     参数:
#     output_file: 输出文件名
#     """
#     # cont-hospital\size-3-unique-sorted.csv
#     # 查找所有size-*.csv文件
#     csv_files = glob.glob('cont-hospital/size-*'+'-unique-sorted.csv')
    
#     if not csv_files:
#         print("未找到size-*.csv文件")
#         return
    
#     # 按文件名排序（确保顺序正确）
#     csv_files.sort()
    
#     print(f"找到以下文件: {csv_files}")
    
#     all_hyperedges = []
    
#     # 读取每个CSV文件
#     for file in csv_files:
#         try:
#             print(f"正在处理文件: {file}")
            
#             # 读取CSV文件
#             df = pd.read_csv(file, header=0)
            
#             # 处理每一行，转换为超边格式
#             for _, row in df.iterrows():
#                 # 移除NaN值并转换为字符串
#                 nodes = [str(int(node)) for node in row if pd.notna(node)]
#                 if nodes:  # 确保行不为空
#                     # 用空格连接节点
#                     hyperedge = ','.join(nodes)
#                     all_hyperedges.append(hyperedge)
                    
#         except Exception as e:
#             print(f"处理文件 {file} 时出错: {e}")
    
#     # 写入输出文件
#     try:
#         with open(output_file, 'w') as f:
#             for hyperedge in all_hyperedges:
#                 f.write(hyperedge + '\n')
        
#         print(f"成功生成文件: {output_file}")
#         print(f"总共处理了 {len(all_hyperedges)} 个超边")
        
#     except Exception as e:
#         print(f"写入输出文件时出错: {e}")

# # # 如果只需要基本功能，也可以使用这个简化版本
# # def simple_combine():
# #     """简化版本的合并函数"""
    
# #     # 获取所有size-*.csv文件并按名称排序
# #     files = sorted([f for f in os.listdir() if f.startswith('size-') and f.endswith('.csv')])
    
# #     with open('combined_hyperedges.txt', 'w') as outfile:
# #         for filename in files:
# #             print(f"处理: {filename}")
# #             with open(filename, 'r') as infile:
# #                 for line in infile:
# #                     # 移除换行符，替换逗号和制表符为空格
# #                     cleaned_line = line.strip().replace(',', ' ').replace('\t', ' ')
# #                     # 移除多余的空格
# #                     cleaned_line = ','.join(cleaned_line.split())
# #                     if cleaned_line:  # 确保行不为空
# #                         outfile.write(cleaned_line + '\n')
    
# #     print("文件合并完成!")

# # 执行合并
# if __name__ == "__main__":
#     # 使用方法1: 使用pandas版本（推荐，更健壮）
#     combine_hyperedge_files()
    
#     # 或者使用方法2: 简化版本
#     # simple_combine()

import pandas as pd

def reindex_hyperedges(csv_file, hyperedge_file, output_file):
    """
    根据CSV文件中的ID顺序重新编号超边文件中的节点索引
    
    参数:
    csv_file: CSV文件路径
    hyperedge_file: 超边文件路径
    output_file: 输出文件路径
    """
    # 读取CSV文件
    df = pd.read_csv(csv_file,header=0 )
    
    # 创建ID到新索引的映射（从1开始）
    id_to_new_index = {}
    for new_index, (_, row) in enumerate(df.iterrows(), 1):
        id_to_new_index[row['id']] = new_index
    
    print("ID映射关系:")
    for old_id, new_index in id_to_new_index.items():
        print(f"{old_id} -> {new_index}")
    
    # 读取并处理超边文件
    with open(hyperedge_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line_num, line in enumerate(f_in, 1):
            line = line.strip()
            if not line:
                continue
                
            # 分割节点ID
            old_ids = [int(x.strip()) for x in line.split(',')]
            
            # 映射到新索引
            new_indices = []
            for old_id in old_ids:
                if old_id in id_to_new_index:
                    new_indices.append(str(id_to_new_index[old_id]))
                else:
                    # 如果ID不在映射中，保持原值（或者可以选择跳过）
                    new_indices.append(str(old_id))
            
            # 写入新文件
            f_out.write(','.join(new_indices) + '\n')
            
            # 打印处理信息（可选）
            if line_num <= 5:  # 只显示前5行的处理结果
                print(f"原始行 {line_num}: {line}")
                print(f"新行 {line_num}: {','.join(new_indices)}")
                print("---")

# 使用示例
if __name__ == "__main__":
  
    # 执行重新索引
    reindex_hyperedges('cont-hospital\labels.csv', 'cont-hospital\combined_hyperedges.txt', 'cont-hospital/reindexed_hyperedges.txt')
    
    print("\n处理完成！")
    print("原始超边文件: hyperedges.txt")
    print("重新索引后的文件: reindexed_hyperedges.txt")