#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

from time import time
from IdfTrainOffline.IDFTrain import IDFClass

if __name__ == "__main__":
    srcFile = "Data\\test1.csv"
    dstFile = "Data\\idf.txt"

    begin = time()
    IDFObj = IDFClass()
    IDFObj.calcIdf(srcFile)
    IDFObj.writeIdf(dstFile)

    elapseTime = time() - begin
    print "Elapsed time:  %.3fs" % elapseTime