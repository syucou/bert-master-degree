#########################################################
#    bert_prediction.sh
#########################################################

#!/bin/bash

arecord -r 16000 -f S16_LE /home/zhu/Desktop/BERT_temporaryname/audio_files/natsu/demo$1.wav -D plughw:1,0 -d 5

date -Ins > time/time610$1_1.txt

dic_dir=~/Downloads/dictation-kit-v4.4

$dic_dir/bin/linux/julius -C $dic_dir/main.jconf -C $dic_dir/am-dnn.jconf \-dnnconf $dic_dir/julius.dnnconf -input file -filelist audio_filelist.txt -outfile

python catch_text.py
    
cd ~/Desktop/BERT_temporaryname/bert_fine_tuning

./bert_prediction.sh

date -Ins > /home/zhu/Desktop/BERT_temporaryname/audio_files/time/time610$1_2.txt

python2 ros_bert.py
