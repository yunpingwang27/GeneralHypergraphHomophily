def get_label_index(file_name):
    hyper_edges = []
    label_index = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.strip().split(' ')
            # int_values = [value for value in values]
            hyper_edges.append(values[1])
            if values[1] == 'M':
                label_index.append(1)
            # elif values[1] == 'F':
                # label_index.append(2)
            else:
                label_index.append(2)
    return label_index
label_index = get_label_index('./original-data/contact-primary-school-classes-gender/label-names-contact-primary-school-classes-gender.txt')
# print(label_index)
from typing import Counter
def get_node_label(file_name,label_index):
    node_label = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            label = int(line.strip())
            node_label.append(label_index[label-1])
    node_class_count = dict(Counter(node_label))
    return node_label,node_class_count
node_label,class_count = get_node_label('./original-data/contact-primary-school-classes-gender/node-labels-contact-primary-school-classes-gender.txt',label_index)
# print(node_label)
print(class_count)
# print()
m=0

def in_label_txt(node_label,file_name):
    with open(file_name, 'w') as file:
        for item in node_label:
            file.write(str(item) + '\n')
file_name = './original-data/contact-primary-school-classes-gender/node-labels-get.txt'
in_label_txt(node_label,file_name)


