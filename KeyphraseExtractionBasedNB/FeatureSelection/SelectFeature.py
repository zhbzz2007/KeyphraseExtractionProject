#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-
import os
from collections import defaultdict
import re
from time import time
import csv

class SelectFeatureClass(object):
    def __init__(self,idfDictPath):
        self._tf = 0
        self._idf = 0
        self._tfidf = 0
        self._idfDict = defaultdict(self._idfValue)
        self._idfDictPath = idfDictPath

    # 如果没有查到这个短语，则idf值设置为默认值10.0
    def _idfValue(self):
        return 10.0

    # 构建包含单词的正则表达式
    def _regexRuleBuild(self,word):
        pattern = re.compile(r'\b' + re.escape(word) + r'(\b|[,;.!?]|\s)',re.IGNORECASE)
        return pattern

    # 查找字符串中包含单词的个数
    def _countWord(self,srcString,word):
        pattern = self._regexRuleBuild(word)
        count = len(pattern.findall(srcString))
        return count

    # 通过正则查找，获取tf值
    def getTf(self,sentence,keyphrase):
        tfValue = self._countWord(sentence,keyphrase)
        tfValue = tfValue * 1.0 / len(sentence.split())
        return tfValue

    # 获取本地的idf词典
    def idfDict(self):
        f = open(self._idfDictPath,"r")
        line = f.readline()
        while line:
            k = line.strip().split("\t")[0]
            v = float(line.strip().split("\t")[1])
            self._idfDict[k] = v
            line = f.readline()

    # 通过idf词典，获取idf值
    def getIdf(self,keyphrase):
        return self._idfDict[keyphrase]

    # 计算tf*idf
    def getTfIdf(self,sentence,keyphrase):
        tfValue = self.getTf(sentence,keyphrase)
        idfValue = self.getIdf(keyphrase)
        return tfValue * idfValue

    # 计算位置特征值
    def getPosition(self,sentence,keyphrase):
        positionValue = sentence.find(keyphrase)
        preList = sentence[:positionValue].split()
        positionValue = (len(preList)) * 1.0 / len(sentence) * 100
        return positionValue

    # 获得该短语的标签，如果为结果短语，则label=1；否则为0
    def getLabel(self,keyphrase,result):
        if keyphrase in result:
            return 1
        else:
            return 0

# 计算特征
def calcFeature(srcFile,dstFile,idfFile):
    fin = open(srcFile,"rb")
    dataset = csv.reader(fin)

    fout = open(dstFile,"wb")
    csv_writer = csv.writer(fout)

    SelectFeatureObj = SelectFeatureClass(idfFile)

    for line in dataset:
        sentence = line[0]
        keyphraseList = line[1].split(";;")
        keyphraseCandidateList = line[3].split(";;")
        tfidfList = []
        positionList = []
        labelList = []

        for ele in keyphraseCandidateList:
            tfidfValue = SelectFeatureObj.getTfIdf(sentence,ele)
            positionValue = SelectFeatureObj.getPosition(sentence,ele)
            labelValue = SelectFeatureObj.getLabel(ele,keyphraseList)
            tfidfList.append(str(tfidfValue))
            positionList.append(str(positionValue))
            labelList.append(str(labelValue))
        # 将结果保存到输出文件，格式为：原始字符串，结果短语，分句后以";;"作为句间分隔符的字符串，候选短语，tfidf数组，位置特征数组，标签数组
        csvLine = (line[0],line[1],line[2],line[3],";;".join(tfidfList),";;".join(positionList),";;".join(labelList))
        csv_writer.writerow(csvLine)

    fin.close()
    fout.close()