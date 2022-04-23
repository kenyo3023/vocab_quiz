import json
import os
import pandas as pd
import numpy as np
from argparse import ArgumentParser


def build_vocab_meta(vocab, vocab_data, col_speech, col_mean):    
    if vocab != vocab_data['單字']:
        print("[%s] given vocab and data not match !!!!!" % vocab)
        return 0
    
    meta = {}
    meta['mean'] = {}
    for speech, mean in zip(col_speech, col_mean):
        if pd.isna(vocab_data[speech]) & pd.isna(vocab_data[mean]):
            continue
        elif pd.isna(vocab_data[speech]) + pd.isna(vocab_data[mean]) == 1:
            print("[%s] invalid speech or mean (one of them is NaN)")
        meta['mean'][vocab_data[speech]] = vocab_data[mean]
    meta['date'] = vocab_data['日期']
    meta['proficiency'] = 1
    return meta

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("file", help="input a csv file to make conversation")
    parser.add_argument("--save", help="the path of output meta file", default="../data/meta")
    args = parser.parse_args()

    vocabs_data = pd.read_csv(args.file)
    vocabs = vocabs_data['單字']
    col_speech = []
    col_mean = []
    max_col_speech = 0
    max_col_mean = 0

    for i, col in enumerate(vocabs_data.columns):
        if '詞性' in col:
            col_speech.append(col)
            max_col_speech += 1
        if '註解' in col:
            col_mean.append(col)
            max_col_mean += 1
    vocabs_meta = {}

    # Start to build the meta of vocabs
    vocabs_count = len(vocabs)
    repeat_vocabs_count = 0
    print("Current size of vocabs : %d" % vocabs_count)
    for i in range(vocabs_count):
        if vocabs[i] in vocabs_meta.keys():
            print("[%s] is already exist" % vocabs[i])
            repeat_vocabs_count += 1
            continue
        vocabs_meta[vocabs[i]] = build_vocab_meta(vocabs[i], vocabs_data.iloc[i], col_speech, col_mean)
    print("New size of vocabs : %d" % (vocabs_count-repeat_vocabs_count))

    # Save the meta of vocabs to .json
    meta_path = args.save
    meta_name = "vocabs.json"
    with open(os.path.join(meta_path, meta_name), 'w') as f:
        json.dump(vocabs_meta, f, indent=4)