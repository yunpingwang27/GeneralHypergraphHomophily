# 同质性比值得分等
line_styles = ['-', '--', '-.', ':', '-']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']
marker_size = 6  # 定义统一的标记大小

# 准备之后改成0.05
import matplotlib.pyplot as plt
import numpy as np
import bisect

def get_result(file_name):
    result = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            result.append(float(line.strip()))
        # result.append(0)
    return result

def plot_result(index, result_A, result_origin_A, label, img_name):
    plt.clf()
    plt.figure(figsize=(7.1, 4.5))

    import numpy as np
    x = np.arange(len(index))
    bar_width = 0.6   # 一样宽，保证重叠
    plt.plot(x, result_origin_A, label=label, marker=markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(x,result_A, label='baseline', marker=markers[2], markersize=marker_size,linestyle = line_styles[1])
    # baseline 作为底层（淡一点）
    # plt.bar(x, result_A, width=bar_width, label='baseline', alpha=0.5)

    # plt.bar(x, result_origin_A, width=bar_width, label=label, alpha=0.7)


    # 原结果覆盖在上面（不透明）

    # plt.xticks(x, index)
    labels = [f"{val:.1f}" for val in index]   # 保留一位小数
    plt.xticks(x, labels)
# 这个x轴要改
    plt.xlabel('s')
    plt.ylabel('Affintiy Score $h_{s,t}(A)$')
    plt.legend()
    plt.grid(axis='y', alpha=0.5)

    plt.tight_layout()
    plt.savefig(img_name)


def plot_biresult(index,result_A,result_B,label,img_name):
    plt.clf()
    plt.plot(index[:],result_A,label = label[0],marker = markers[0], markersize=marker_size)
    plt.plot(index[:],result_B,label = label[1],marker = markers[1], markersize=marker_size)
    plt.xlabel('s')
    plt.ylabel('$m_{[s,1]}/m_{[0,1]}$')
    plt.legend()
    plt.grid(alpha = 0.5)
    plt.savefig(img_name)

def get_divide(a,b):
    plot_data = []
    for i in range(len(a)):
        if a[i] == b[i]:
                # b[i] = 1
                plot_data.append(1)
        else:
            if b[i]==0 and a[i] != 0:
            # else:
                b[i] = 0.01 
                # b[i] = 0.01 
                plot_data.append(a[i]/b[i])
            elif a[i] == 0 and b[i] !=0:
                if b[i]<0.01:
                # a[i] = 0.01
                    plot_data.append(1)
                else:
                    plot_data.append(a[i]/b[i])
            else:
                plot_data.append(a[i]/b[i])
    return plot_data

def get_normalized_bias(a,b):
    bias_list = []
    for i in range(len(a)):
        bias = a[i]-b[i]
        if a[i]-b[i] >=0:
            bias = bias/(1-b[i])
        else:
            bias = bias/b[i]
        bias_list.append(bias)
    return bias_list

def get_diff(result):
    result.append(0)
    result = [result[i]-result[i+1] for i in range(len(result)-1)]
    return result

def plot(index,result_A,result_B,label,image_name = 'result_A_B_diff.png',horb = 'h'):
    plt.clf()
    plt.plot(index[:],result_A[:],label = label[0],marker = markers[0], markersize=marker_size)
    plt.plot(index[:],result_B[:],label = label[1],marker = markers[2], markersize=marker_size)
    plt.xlabel('s')
    if horb == 'h':
        plt.ylabel('$h_{s,t}(X)$')
    else:
        plt.ylabel('$b_{s,t}(X)$')
    plt.legend()
    plt.grid(alpha = 0.5)
    plt.savefig(image_name)
    plt.clf()

def plt_h_b(index,plot_data_A,plot_data_B,label,image_name = 'h_b.png',gap = 0.05,symmet =True):
    def custom_tick_formatter(value):
        if value == symmetry:
            return str(value)
        if value!= symmetry:
            return f"{value:.1f}"

    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    # plt.plot(index[:],plot_data_A[:],label = label[0],marker = markers[0], markersize=marker_size,color = 'k')
    plt.plot(index[:],plot_data_A[:],label = label[0],marker = markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(index[:],plot_data_B[:],label = label[1],marker = markers[2], markersize=marker_size,linestyle = line_styles[1])
    
    symmetry = (1-gap)/2
    x_ticks = [0, 0.2, 0.4,0.6,0.8]  
    # if symmet == True:
    #     bisect.insort(x_ticks, symmetry)
    #     plt.xticks(x_ticks, [custom_tick_formatter(tick) for tick in x_ticks])
    #     plt.axvline(x=symmetry, linestyle='--', label=f'Axis of symmetry at s={symmetry}')
    # else:
    plt.xticks(x_ticks)
    
    plt.axhline(y=1, linestyle='dashed', color='darkred', label='Value 1')
    plt.ylabel('Homophily Score $H_{s,t}(X)$')
    plt.xlabel('s')
    plt.yscale('log')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(image_name)
    plt.clf()

def plt_all(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label,folder = './figure/congress/congress',symmet = True):
    for k in range(1,k_max+1):
        s_r = [k]
        index = []
        for value in np.arange(0,1,gap):
            index.append(value)
    plot_result(index,result_A,result_origin_A,label=label[0],img_name = folder+'_result_A.png')
    plot_result(index,result_B,result_origin_B,label[1],img_name=folder+'_result_B.png')
    plot_biresult(index,result_A,result_B,label=label,img_name=folder+'_biresult.png')

    plot(index,result_A,result_B,label,image_name=folder+'_result_A_B_diff.png')
    plot(index,result_origin_A,result_origin_B,label,image_name=folder+'_b_A_B_diff.png',horb= 'b')

    plot_data_A  = get_divide(result_origin_A,result_A)
    plot_data_B  = get_divide(result_origin_B,result_B)
    print(plot_data_A)
    print(plot_data_B)

    # plt_h_b(index,plot_data_A,plot_data_B,label,image_name=folder+'_h_b.png',gap = gap,symmet=symmet,color = 'k')
    plt_h_b(index,plot_data_A,plot_data_B,label,image_name=folder+'_h_b.png',gap = gap,symmet=symmet)
    plot_data_A  = get_normalized_bias(result_origin_A,result_A)
    plot_data_B  = get_normalized_bias(result_origin_B,result_B)
    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    plt.plot(index[:],plot_data_A[:],label = label[0],marker = markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(index[:],plot_data_B[:],label = label[1],marker = markers[2], markersize=marker_size,linestyle = line_styles[1])
    plt.ylabel('Normalized Bias Score $f_{s,t}(X)$')
    plt.xlabel('s')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(folder+'_normalized_bias_score.png')
def plt_all_t_ana(result_A,result_B,result_origin_A,result_origin_B,gap,k_max,label,folder = './figure/congress/congress',symmet = True):
    for k in range(1,k_max+1):
        s_r = [k]
        index = []
        for value in np.arange(0,1,gap):
            index.append(value)
    plot_result(index,result_A,result_origin_A,label=label[0],img_name = folder+'_result_A.png')
    plot_result(index,result_B,result_origin_B,label[1],img_name=folder+'_result_B.png')
    plot_biresult(index,result_A,result_B,label=label,img_name=folder+'_biresult.png')

    plot(index,result_A,result_B,label,image_name=folder+'_result_A_B_diff.png')
    plot(index,result_origin_A,result_origin_B,label,image_name=folder+'_b_A_B_diff.png',horb= 'b')

    plot_data_A  = get_divide(result_origin_A,result_A)
    plot_data_B  = get_divide(result_origin_B,result_B)
    print(plot_data_A)
    print(plot_data_B)

    # plt_h_b(index,plot_data_A,plot_data_B,label,image_name=folder+'_h_b.png',gap = gap,symmet=symmet,color = 'k')
    plt_h_b(index,plot_data_A,plot_data_B,label,image_name=folder+f'_h_b_{gap}.png',gap = gap,symmet=symmet)
    plot_data_A  = get_normalized_bias(result_origin_A,result_A)
    plot_data_B  = get_normalized_bias(result_origin_B,result_B)
    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    plt.plot(index[:],plot_data_A[:],label = label[0],marker = markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(index[:],plot_data_B[:],label = label[1],marker = markers[2], markersize=marker_size,linestyle = line_styles[1])
    plt.ylabel('normalized_bias_score')
    plt.xlabel('s')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(folder+f'_normalized_bias_score_{gap}.png')

def plt_h_b1(index,plot_data_A,plot_data_B,plot_data_C,label,image_name = 'h_b.png',gap = 0.05,symmet =True):
    def custom_tick_formatter(value):
        if value == symmetry:
            return str(value)
        if value!= symmetry:
            return f"{value:.1f}"

    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    plt.plot(index[:],plot_data_A[:],label = label[0], marker=markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(index[:],plot_data_B[:],label = label[1], marker=markers[1], markersize=marker_size,linestyle = line_styles[1])
    plt.plot(index[:],plot_data_C[:],label = label[2], marker=markers[2], markersize=marker_size,linestyle = line_styles[2])
    
    symmetry = (1-gap)/2
    x_ticks = [0, 0.2, 0.4,0.6,0.8]  
    if symmet == True:
        bisect.insort(x_ticks, symmetry)
        plt.xticks(x_ticks, [custom_tick_formatter(tick) for tick in x_ticks])
        plt.axvline(x=symmetry, linestyle='--', label=f'Axis of symmetry at s={symmetry}')
    else:
        plt.xticks(x_ticks)
    
    plt.axhline(y=1, linestyle='dashed', color='darkred', label='Value 1')
    plt.ylabel('Homophily Score $H_{s,t}(X)$')
    plt.xlabel('s')
    plt.yscale('log')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(image_name)
    plt.clf()

def plt_h_b2(index,plot_data_A,plot_data_B,plot_data_C,plot_data_D,plot_data_E,label,image_name = 'h_b.png',gap = 0.05,symmet =True):
    def custom_tick_formatter(value):
        if value == symmetry:
            return str(value)
        if value!= symmetry:
            return f"{value:.1f}"

    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    plt.plot(index[:],plot_data_A[:],label = label[0], marker=markers[0], markersize=marker_size)
    plt.plot(index[:],plot_data_B[:],label = label[1], marker=markers[1], markersize=marker_size)
    plt.plot(index[:],plot_data_C[:],label = label[2], marker=markers[2], markersize=marker_size)
    plt.plot(index[:],plot_data_D[:],label = label[3], marker=markers[3], markersize=marker_size)
    plt.plot(index[:],plot_data_E[:],label = label[4], marker=markers[4], markersize=marker_size)
    
    symmetry = (1-gap)/2
    x_ticks = [0, 0.2, 0.4,0.6,0.8]  
    if symmet == True:
        bisect.insort(x_ticks, symmetry)
        plt.xticks(x_ticks, [custom_tick_formatter(tick) for tick in x_ticks])
        plt.axvline(x=symmetry, linestyle='--', label=f'Axis of symmetry at s={symmetry}')
    else:
        plt.xticks(x_ticks)
    
    plt.axhline(y=1, linestyle='dashed', color='darkred', label='Value 1')
    plt.ylabel('Homophily Score $H_{s,t}(X)$')
    plt.xlabel('s')
    plt.yscale('log')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(image_name)
    plt.clf()

def plt_h_b_all(index,plot_data,class_num,label,image_name = 'h_b.png',gap = 0.05,symmet =True):
    def custom_tick_formatter(value):
        if value == symmetry:
            return str(value)
        if value!= symmetry:
            return f"{value:.1f}"

    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    for i in range(class_num):
        plt.plot(index[:],plot_data[i][:],label = "class "+chr(i+1+64),linestyle = line_styles[i],color = colors[i],marker = markers[i], markersize=marker_size)
    
    symmetry = (1-gap)/2
    x_ticks = [0, 0.2, 0.4,0.6,0.8]  
    if symmet == True:
        bisect.insort(x_ticks, symmetry)
        plt.xticks(x_ticks, [custom_tick_formatter(tick) for tick in x_ticks])
        plt.axvline(x=symmetry, linestyle='--', label=f'Axis of symmetry at s={symmetry}')
    else:
        plt.xticks(x_ticks)
    
    plt.axhline(y=1, linestyle='dashed', color='darkred', label='Value 1')
    plt.ylabel('Homophily Score $H_{s,t}(X)$')
    plt.xlabel('s')
    plt.yscale('log')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(image_name)
    plt.clf()

def plt_all1(result_A,result_B,result_C,result_origin_A,result_origin_B,result_origin_C,gap,k_max,label,folder = './figure/congress/congress',symmet = True):
    for k in range(1,k_max+1):
        s_r = [k]
        index = []
        for value in np.arange(0,1,gap):
            index.append(value)
    
    plot_result(index,result_A,result_origin_A,label=label[0],img_name = folder+'_result_A.png')
    plot_result(index,result_B,result_origin_B,label[1],img_name=folder+'_result_B.png')
    plot_result(index,result_C,result_origin_C,label[2],img_name=folder+'_result_B.png')

    plot_data_A  = get_divide(result_origin_A,result_A)
    plot_data_B  = get_divide(result_origin_B,result_B)
    plot_data_C  = get_divide(result_origin_C,result_C)
    
    print(plot_data_A)
    print(plot_data_B)

    plt_h_b1(index,plot_data_A,plot_data_B,plot_data_C,label,image_name=folder+'_h_b.png',gap = gap,symmet=symmet)
    plot_data_A  = get_normalized_bias(result_origin_A,result_A)
    plot_data_B  = get_normalized_bias(result_origin_B,result_B)
    plot_data_C  = get_normalized_bias(result_origin_C,result_C)
    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    plt.plot(index[:],plot_data_A[:],label = label[0], marker=markers[0], markersize=marker_size,linestyle = line_styles[0])
    plt.plot(index[:],plot_data_B[:],label = label[1], marker=markers[1], markersize=marker_size,linestyle = line_styles[1])
    plt.plot(index[:],plot_data_C[:],label = label[2], marker=markers[2], markersize=marker_size,linestyle = line_styles[2])
    plt.ylabel('Normalized Bias Score $f_{s,t}(X)$')
    plt.xlabel('s')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(folder+'_normalized_bias_score.png')

def plt_all2(result,result_origin,class_num,gap,k_max,label,folder = './figure/congress/congress',symmet = False):
    for k in range(1,k_max+1):
        s_r = [k]
        index = []
        for value in np.arange(0,1,gap):
            index.append(value)
    
    plot_data = []
    for i in range(class_num):
        plot_data.append(get_divide(result_origin[i],result[i]))
    print(plot_data)

    plt_h_b_all(index,plot_data,class_num,label,image_name=folder+'_h_b.png',gap = gap,symmet=symmet)
    
    plot_data = []
    plt.clf()
    plt.figure(figsize= (7.1,4.5))
    for i in range(class_num):
        plot_data_A  = get_normalized_bias(result_origin[i],result[i])
        plt.plot(index[:],plot_data_A[:],label = "class "+chr(i+1+64),color = colors[i],marker = markers[i],linestyle = line_styles[i//2], markersize=marker_size)
    
    plt.ylabel('Normalized Bias Score $f_{s,t}(X)$')
    plt.xlabel('s')
    plt.grid(alpha = 0.5)
    plt.legend()
    plt.savefig(folder+'_normalized_bias_score.png')