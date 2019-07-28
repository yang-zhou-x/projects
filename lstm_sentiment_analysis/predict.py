# -*- coding: utf-8 -*-
'''
This module is used for predicting.

@Time    :   2019
@Author  :   ZHOU, YANG  
@Contact :   yzhou0000@gmail.com
'''

import os
import pickle
import numpy as np
from keras.models import load_model
import preprocess as pp

# Parameters
dict_size = 10000
max_sequence_len = 30  # 序列对齐的长度
batch_size = 64

stopwords_name = 'cn_stopwords_punctuations.csv'
model_name = f'lstm-{max_sequence_len}.hdf5'
tokenizer_name = f'tokenizer-{dict_size}.pickle'
test_name = 'test.txt'
outputs_name = 'result.txt'

# Paths
init_path = os.getcwd()

data_dir = os.path.join(init_path, 'datasets')
stopwords_path = os.path.join(data_dir, stopwords_name)
test_path = os.path.join(data_dir, test_name)
outputs_path = os.path.join(data_dir, outputs_name)

save_dir = os.path.join(init_path, 'saved_models')
model_path = os.path.join(save_dir, model_name)
tokenizer_path = os.path.join(save_dir, tokenizer_name)

# load data
with open(test_path, encoding='utf-8') as f:
    texts = f.readlines()
texts = [x.strip() for x in texts]

# tokenize
stopwords = pp.get_stopwords(stopwords_path)
texts = pp.tokenize_texts(texts, stopwords)

# to sequences
with open(tokenizer_path, 'rb') as t:
    tokenizer = pickle.load(t)
x, _ = pp.texts_to_sequence_vectors(texts, max_sequence_len,
                                    tokenizer=tokenizer)

# load model
model = load_model(model_path, compile=True)

# predict
y_pred = model.predict(x,
                       batch_size=batch_size,
                       verbose=1)
y_pred = ['正面' if x[0] > 0.5 else '负面' for x in y_pred.tolist()]

# output
y_pred = [x + '\n' for x in y_pred]
with open(outputs_path, 'w') as f:
    f.writelines(y_pred)
