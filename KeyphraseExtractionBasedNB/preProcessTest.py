#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

from time import time
from Preprocess.preProcess import processText

def test():
    srcFile = "Data\\docstring.csv"
    dstFile = "Data\\test1.csv"

    begin = time()
    processText(srcFile,dstFile)
    end = time() - begin
    print "time:",end

if __name__ == "__main__":
    test()