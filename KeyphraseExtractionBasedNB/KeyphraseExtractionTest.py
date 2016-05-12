#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

import os
from Classifier.NaiveBayes import NBClassifier
from time import time
import csv
import random
from collections import defaultdict

class KeyphraseExtractionClass(object):
    def __init__(self):
        pass

    # 分割数据集为训练数据集，验证数据集，测试数据集
    def splitDataset(self,dataset,splitRatio):
        # 将数据集随机乱序
        random.shuffle(dataset)
        # 将数据集最后100篇文献作为测试数据集
        testset = dataset[-100:]
        splitLen = int((len(dataset) - 100 ) * splitRatio)
        trainset = dataset[:splitLen]
        validset = dataset[splitLen:-100]
        return trainset,validset,testset

    # 提取数据，主要针对训练数据集和验证数据集
    def extractData(self,dataset):
        datasetNew = []
        temp = []
        for line in dataset:
            tfidfValue = line[4].split(";;")
            posValue = line[5].split(";;")
            labelValue = line[6].split(";;")
            for tfidf,pos,label in zip(tfidfValue,posValue,labelValue):
                temp = []
                temp.append(float(tfidf))
                temp.append(float(pos))
                temp.append(int(label))
                datasetNew.append(temp)
        return datasetNew

    # 提取数据，主要针对测试数据集
    def extractDataForTest(self,dataset):
        datasetNew = defaultdict(list)
        docList = []
        temp = []
        for line in dataset:
            docList =[]
            sentence = line[0]
            tfidfValue = line[4].split(";;")
            posValue = line[5].split(";;")
            keyphraseCandidate = line[3].split(";;")
            for tfidf,pos,keyphrase in zip(tfidfValue,posValue,keyphraseCandidate):
                temp = []
                temp.append(keyphrase)
                temp.append(float(tfidf))
                temp.append(float(pos))
                docList.append(temp)
            datasetNew[sentence] = docList
            datasetNew[sentence].append(line[1])
        return datasetNew

    # 基于Naive Bayes分类器的关键短语抽取主函数
    def keyphraseExtractionBasedNB(self,srcFile,dstFile,keyphraseNum = 10):
        fin = open(srcFile,"rb")
        lines = csv.reader(fin)
        fout = open(dstFile,"wb")

        dataset = []
        for line in lines:
            dataset.append(line)
        # 数据集分割比例
        ratio = 0.7

        trainset,validset,testset = self.splitDataset(dataset,ratio)
        trainset = self.extractData(trainset)
        validset = self.extractData(validset)
        testset = self.extractDataForTest(testset)

        # 初始化Naive Bayes分类器
        NBClassifierObj = NBClassifier()
        # 训练数据
        NBClassifierObj.train(trainset)
        # 预测数据
        predictions = NBClassifierObj.predict(validset)
        # 在验证数据集上计算分类正确率
        print NBClassifierObj.accuracy(predictions,validset)

        for key,value in testset.items():
            resultDict = {}
            resultKeyphrase = []
            docList = value[0:-1]
            keyphraseResult = value[-1]
            for temp in docList:
                # 利用训练好的分类器，输入每个短语对应的特征向量，获得标签
                label,pro = NBClassifierObj.getLabel(temp[1:3])
                # 将标签值为1的短语添加到结果短语中
                if label:
                    resultDict[temp[0]] = pro
                    # print temp,label,pro
            # 根据概率密度值降序进行排列
            resultDict = sorted(resultDict.items(),key = lambda resultDict:resultDict[1],reverse = True)
            # 输出指定数目的结果短语
            keyphraseTest = [ele[0] for ele in resultDict][:keyphraseNum]
            fout.write(key + "\n")
            fout.write(keyphraseResult + "\n")
            fout.write(";;".join(keyphraseTest) + "\n\n")
        fout.close()
        fin.close()

def test():
    begin = time()
    srcFile = os.path.join("Data","test2.csv")
    dstFile = os.path.join("Result","result.txt")
    keyphraseNum = 10
    KeyphraseExtractionObj = KeyphraseExtractionClass()
    KeyphraseExtractionObj.keyphraseExtractionBasedNB(srcFile,dstFile,keyphraseNum)
    end = time() - begin
    print "time:",end

if __name__ == "__main__":
    test()
