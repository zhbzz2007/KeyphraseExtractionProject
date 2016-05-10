#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

import os
import re
import nltk
import csv
from time import time
sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

from StopWords.stopword import STOP_WORDS

# 构造候选短语词性组合
# grammer = r"""NP: {<NN|NNS|NNP|NNPS|JJ|JJR|JJS>*<NN|NNS|NNP|NNPS>}"""
grammer = "NP: {<NN.*|JJ.*>*<NN.*>}"
cp = nltk.RegexpParser(grammer)

#抽取出候选短语
def extracKeyphraseCandidate(pos_token):
    keyphraseCandidate = []
    for keyphraseEle in cp.parse(pos_token):
        if not isinstance(keyphraseEle,tuple):
            temp = [ele[0] for ele in keyphraseEle]
            tempStr = ' '.join(temp)
            # 第一个单词或者最后一个单词不是停用词
            if temp[0] in STOP_WORDS or temp[-1] in STOP_WORDS:
                continue
            # 短语的字符数多于1个
            if len(tempStr) <= 1:
                continue
            # 短语的单词数不多于6个
            if 1 <= len(temp) <= 6:
                keyphraseCandidate.append(tempStr)
    return keyphraseCandidate

#处理输入文件
def processText(srcFile,dstFile):
    fin = open(srcFile,"rb")
    dataset = csv.reader(fin)

    fout = open(dstFile,"wb")
    csv_writer = csv.writer(fout)

    for line in dataset:
        keyphraseCandidate = []
        # 分句
        SentenceList = sent_tokenizer.tokenize(line[0])

        for sentence in SentenceList:
            # 对每一句进行分词
            token = nltk.word_tokenize(sentence)
            # 词性标注
            pos_token = nltk.pos_tag(token)
            # 提取候选短语
            keyphraseCandidate.extend(extracKeyphraseCandidate(pos_token))
        keyphraseCandidate = list(set(keyphraseCandidate))

        # 将结果保存到输出文件，格式为：原始字符串，结果短语，分句后以";;"作为句间分隔符的字符串，候选短语
        csvLine = (line[0],line[1],";;".join(SentenceList),";;".join(keyphraseCandidate))
        csv_writer.writerow(csvLine)

    fin.close()
    fout.close()