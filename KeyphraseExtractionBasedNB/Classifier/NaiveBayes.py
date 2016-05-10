#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-
from collections import defaultdict
import math

# 构造Naive Bayes 分类器
class NBClassifier(object):
    def __init__(self):
        self._parameter = {}
        self._classProb = defaultdict(int)
        self._separateData = defaultdict(list)

    # 按照类别对数据进行分类
    def _separateClass(self,dataset):
        for item in dataset:
            label = item[-1]
            self._separateData[label].append(item[:-1])
            self._classProb[label] += 1

    # 计算样本的平均值
    def _mean(self,numbers):
        return sum(numbers) / float(len(numbers))

    # 计算样本的均方差
    def _std(self,numbers):
        mean = self._mean(numbers)
        std = sum([pow(x-mean,2) for x in numbers]) / float(len(numbers) - 1)
        return math.sqrt(std)

    # 针对每一类别，计算相应特征属性的参数
    def _parameterTrain(self,dataset):
        parameter = [(self._mean(attribute),self._std(attribute)) for attribute in zip(*dataset)]
        return parameter

    # 训练参数
    def train(self,dataset):
        self._separateClass(dataset)
        for classValue,prob in self._classProb.items():
            self._classProb[classValue] = (self._classProb[classValue] + 1) * 1.0 / (len(dataset) + 2)

        for classValue,instance in self._separateData.items():
            self._parameter[classValue] = self._parameterTrain(instance)

    # 计算一个样本的概率密度值
    def _calculateAttrProbability(self,mean,std,x):
        temp = math.exp( -(pow(x-mean,2) / (2 * pow(std,2))) )
        return temp / float(math.sqrt(2*math.pi) * std)

    # 计算输入样本在各个类别下的概率密度值，并归一化
    def _calculateClassProbability(self,inputVector):
        probability = {}
        for classValue,parameterList in self._parameter.items():
            # probability[classValue] = self._classProb[classValue]
            probability[classValue] = 1
            for index,parameter in enumerate(parameterList):
                mean,std = parameter
                pro = self._calculateAttrProbability(mean,std,inputVector[index])
                probability[classValue] *= pro
        Sum = sum(probability.values())
        probabilityNew = {}
        for k,v in probability.items():
            probabilityNew[k] = v * 1.0 / Sum
        return probabilityNew

    # 找出概率密度值最大值，并将其类别作为样本的类别
    def getLabel(self,inputVector):
        probability = self._calculateClassProbability(inputVector)
        bestPro,bestLabel = -1,None
        for classValue,pro in probability.items():
            if bestLabel == None or pro > bestPro:
                bestPro = pro
                bestLabel = classValue
        return bestLabel,bestPro

    # 对测试集进行预测
    def predict(self,testset):
        predictions = []
        for data in testset:
            label,pro = self.getLabel(data)
            predictions.append(label)
        return predictions

    # 计算分类准确率
    def accuracy(self,predictions,testset):
        correction = 0
        for index,data in enumerate(testset):
            if data[-1] == predictions[index]:
                correction += 1
        return correction / float(len(testset)) * 100