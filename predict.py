#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : predict.py
@Time : 2018/12/14 17:35
@Site : 
@Software: PyCharm
'''

from MaxEnt import MaxEnt

# 文件输入
maxent = MaxEnt()
maxent.loadModel()
maxent.predictFile('testFeature.txt', 'result.txt')

# 单个句子输入
# print(maxent.predictSentence("藏	    们	收	北	京	收/藏	藏/北	们/收/藏	藏/北/京	们/收/藏/北/京"))
# print(maxent.predictSentence("北	    收	藏	京	史	藏/北	北/京	收/藏/北	北/京/史	收/藏/北/京/史"))
# print(maxent.predictSentence("京	    藏	北	史	料	北/京	京/史	藏/北/京	京/史/料	藏/北/京/史/料"))
# print(maxent.predictSentence("史	    北	京	料	中	京/史	史/料	北/京/史	史/料/中	北/京/史/料/中"))
