#########################################################
#    bert_prediction.sh
#########################################################

#!/bin/bash

export BERT_BASE_DIR=/home/zhu/Desktop/BERT_temporaryname/Japanese_L-12_H-768_A-12_E-30_BPE_WWM
export DATA_DIR=/home/zhu/Desktop/BERT_temporaryname/datasets
export TRAINED_CLASSIFIER=/home/zhu/Desktop/BERT_temporaryname/bert_output/bert_output_d_400

python /home/zhu/Desktop/BERT_temporaryname/bert/run_classifier.py \
  --task_name=roco \
  --do_predict=true \
  --data_dir=$DATA_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/config.json \
  --init_checkpoint=$TRAINED_CLASSIFIER \
  --max_seq_length=128 \
  --output_dir=$TRAINED_CLASSIFIER/
