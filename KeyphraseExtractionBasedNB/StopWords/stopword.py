#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

import os
import linecache

STOP_WORDS = set()

STOP_WORDS = set(ele.lower().strip() for ele in linecache.getlines(os.path.join(os.getcwd(),"EnglishStopWord.txt")))