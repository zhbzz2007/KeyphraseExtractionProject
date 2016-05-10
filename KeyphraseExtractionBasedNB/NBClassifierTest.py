#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

import csv
import random

from Classifier.NativeBayes import NBClassifier

def loadCsv(filename):
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset
 
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]

if __name__ == "__main__":

    filename = 'Data\\iris.csv'
    splitRatio = 0.5
    dataset = loadCsv(filename)
    for i in range(1):
        trainingSet, testSet = splitDataset(dataset, splitRatio)

        NBClassifierObj = NBClassifier()
        NBClassifierObj.train(trainingSet)
        predictions = NBClassifierObj.predict(testSet)
        print NBClassifierObj.accuracy(predictions,testSet)