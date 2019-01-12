#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : Score.py
@Time : 2018/12/11 20:04
@Site : 
@Software: PyCharm
'''


def score(result, test):
    reFile = open(result, 'r', encoding="utf-8")
    teFile = open(test, 'r', encoding="utf-8")
    counter = 0
    org = 0
    per = 0
    loc = 0
    reOrg = 0
    rePer = 0
    reLoc = 0
    rightOrg = 0
    rightPer = 0
    rightLoc = 0
    dic = {'B-ORG', 'I-ORG', 'B-PER', 'I-PER', 'B-LOC', 'I-LOC'}
    for reLine in reFile.readlines():
        reLine = reLine.strip().split('\t')
        teLine = teFile.readline().strip().split('\t')
        if len(reLine) <= 1 or len(reLine[0]) == 0:
            continue
        if 'ORG' in teLine[1]:
            org = org + 1
        if 'PER' in teLine[1]:
            per = per + 1
        if 'LOC' in teLine[1]:
            loc = loc + 1

        if 'ORG' in reLine[1]:
            reOrg = reOrg + 1
        if 'PER' in reLine[1]:
            rePer = rePer + 1
        if 'LOC' in reLine[1]:
            reLoc = reLoc + 1
        if reLine[1] == teLine[1] and 'ORG' in reLine[1]:
            rightOrg = rightOrg + 1
        if reLine[1] == teLine[1] and 'PER' in reLine[1]:
            rightPer = rightPer + 1
        if reLine[1] == teLine[1] and 'LOC' in reLine[1]:
            rightLoc = rightLoc + 1

    reFile.close()
    teFile.close()
    sum1 = org + per + loc
    print("标准答案中ORG,PER,LOC: ", org, per, loc, "总个数：", sum1)
    sum2 = reOrg + rePer + reLoc
    print("测试结果中ORG,PER,LOC: ", reOrg, rePer, reLoc, "总个数：", sum2)
    sum3 = rightPer + rightLoc + rightOrg
    print("测试正确ORG,PER,LOC: ", rightOrg, rightPer, rightLoc, "总个数：", sum3)


if __name__ == "__main__":
    score('result.txt', 'data/test_data')
