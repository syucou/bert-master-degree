#########################################################
#    catch_text.py
#########################################################

path_r = '/home/zhu/Desktop/BERT_temporaryname/audio_files/natsu/demo6.out'

path_w = '/home/zhu/Desktop/BERT_temporaryname/datasets/dataset_demo.csv'

import pandas as pd
import numpy as np
import csv

with open(path_r) as f:
    s = f.readlines()

s = s[0].strip('sentence1:').strip()
print(s)

with open(path_w, 'w') as f:
    writer = csv.writer(f)
    writer.writerow([s, 1])

