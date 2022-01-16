#########################################################
#    make_dataset.py
#########################################################

import csv
import random

output_reader = []
output_train = []
output_dev = []
output_test = []

with open('/home/zhu/Desktop/BERT_temporaryname/datasets/set_data.csv') as f:
    reader = csv.reader(f)
    lines = [row for row in reader]
    #print(lines)
    len_lines = len(lines) #print(len_lines)
    for i in range(len_lines):
        line = lines[i]#.split('\t')
        output_reader.append(line)

    #print(output_reader)
    #print(line)

def output_data(num, list_output):        
    for i in range(num):
        l = random.choice(output_reader)#print(l)
        output_reader.remove(l)#print(len(output_reader))
        list_output.append(l)
        i += 1

def write_data(route, output_set):
    print(output_set)
    with open(route, 'a') as f:
        writer = csv.writer(f)
        for i in range(len(output_set)):
            writer.writerow([output_set[i][0], output_set[i][1]])
            #writer.writerow([output_set[i]])

# dev, test, train dataのデータ量を変える
output_data(400, output_train)
output_data(100, output_dev)
#output_data(50, output_test)

write_data('/home/zhu/Desktop/BERT_temporaryname/datasets/set_train_data_400.csv', output_train)
write_data('/home/zhu/Desktop/BERT_temporaryname/datasets/set_dev_data_100.csv', output_dev)
#write_data('/home/zhu/Desktop/BERT_temporaryname/datasets/set_test_n_100_v3.csv', output_test)
#print(len(output_reader))
