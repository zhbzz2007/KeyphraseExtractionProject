#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-
from time import time
from FeatureSelection.SelectFeature import calcFeature

def test():
    srcFile = "Data\\test1.csv"
    dstFile = "Data\\test2.csv"

    idfFile = "Data\\idf.txt"

    begin = time()
    calcFeature(srcFile,dstFile,idfFile)
    end = time() - begin
    print "time:",end

if __name__ == "__main__":
    test()