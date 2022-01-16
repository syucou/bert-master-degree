#########################################################
#    bert_fine_tuning.sh
#########################################################

#!/bin/bash

export BERT_BASE_DIR=/home/zhu/Desktop/BERT_temporaryname/Japanese_L-12_H-768_A-12_E-30_BPE_WWM
export DATA_DIR=/home/zhu/Desktop/BERT_temporaryname/datasets


python /home/zhu/Desktop/BERT_temporaryname/bert/run_classifier.py \
  --task_name=roco \
  --do_train=true \
  --do_eval=true \
  --data_dir=$DATA_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/config.json \
  --init_checkpoint=$BERT_BASE_DIR/model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=100.0 \
  --output_dir=/home/zhu/Desktop/BERT_temporaryname/bert_output/bert_output_d_400
