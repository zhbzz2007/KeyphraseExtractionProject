#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

from collections import defaultdict
import re
from math import log
from time import time
import os
import csv

class IDFClass(object):
    def __init__(self):
        self._idfDict = defaultdict(int)
        self._wordSet = set()
        self._docCount = 0
        self._content = []

    # 构建包含单词的正则表达式
    def _regexRuleBuild(self,word):
        pattern = re.compile(r'\b' + re.escape(word) + r'(\b|[,;.!?]|\s)',re.IGNORECASE)
        return pattern

    # 查找字符串中是否包含此单词
    def _findWord(self,srcString,word):
        pattern = self._regexRuleBuild(word)
        match = pattern.search(srcString)
        if match:
            return True
        else:
            return False

    # 构建不重复的单词表
    def _uniqueWord(self,dataset):
        for line in dataset:
            self._docCount += 1
            self._content.append(line[0])

            wordList = line[0].split()
            for wordEle in wordList:
                self._wordSet.add(wordEle)

            keyphraseList = line[1].split(";;")
            for keyphraseEle in keyphraseList:
                self._wordSet.add(keyphraseEle)

            keyphraseList2 = line[3].split(";;")
            for keyphraseEle in keyphraseList2:
                self._wordSet.add(keyphraseEle)

        print "总记录数目：",self._docCount
        print "短语数目：",len(self._wordSet)

    # 计算idf值
    def calcIdf(self,srcFilePath):
        fin = open(srcFilePath,"rb")
        dataset = csv.reader(fin)

        self._uniqueWord(dataset)
        count = 0
        for word in self._wordSet:
            df = 0
            for line in self._content:
                if self._findWord(line,word):
                    df += 1
            count += 1
            if count % 500 == 0:
                print count
            self._idfDict[word] = log( (self._docCount + 1) * 1.0 / (df + 1) , 2) 

    # 保存idf值
    def writeIdf(self,dictPath):
        fout = open(dictPath,"w")
        temp = self._idfDict
        temp1 = sorted(temp.items(),key = lambda temp:temp[1],reverse = True)
        for item in temp1:
            fout.write(item[0] + "\t" + str(item[1]) + "\n")
        fout.close()

    # 返回idf词典
    def dict(self):
        return self._idfDict