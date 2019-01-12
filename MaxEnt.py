#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : MaxEnt.py
@Time : 2018/12/11 12:09
@Site : 
@Software: PyCharm
'''

import time
import sys
import math
from collections import defaultdict
import pickle


class MaxEnt:
    def __init__(self):
        self._samples = []  # 样本集, 元素是[y,x1,x2,...,xn]的元组
        self._Y = set([])  # 标签集合，相当于去重之后的y
        self._numXY = defaultdict(int)  # key是(xi,yi)对，value是count(xi,yi)
        self._N = 0  # 样本数量
        self._n = 0  # 特征对(xi,yi)总数量
        self._xyID = {}  # 对（x，y）对做的顺序编号(ID)，key是(xi,yi)对，value是ID
        self._C = 0  # 样本最大的特征数量，用于求参数的迭代
        self._ep_ = []  # 样本分布的特征期望值
        self._ep = []  # 模型分布的特征期望值
        self._w = []  # 对应n个特征的权值
        self._lastw = []  # 上一轮迭代的权值
        self._EPS = 0.01  # 判断是否收敛的阈值

    def load_data(self, filename):
        '''
        加载训练数据
        :param filename: 训练文件
        :return:
        '''
        for line in open(filename, "r", encoding="utf-8"):
            sample = line.strip().split("\t")
            if len(sample) < 2:  # 至少：标签+一个特征
                continue
            y = sample[0]
            X = sample[1:]  # 特征
            self._samples.append(sample)
            self._Y.add(y)  # label
            for x in set(X):  # set给X去重
                self._numXY[(x, y)] += 1

    def _initparams(self):
        '''
        初始化参数
        :return:
        '''
        self._N = len(self._samples)
        self._n = len(self._numXY)  # 没有做任何特征提取操作，直接操作特征
        self._C = max([len(sample) - 1 for sample in self._samples])
        self._w = [0.0] * self._n
        self._lastw = self._w[:]
        self._sample_ep()

    def _convergence(self):
        '''
        判断是否收敛
        :return:
        '''
        for w, lw in zip(self._w, self._lastw):
            print(math.fabs(w - lw))
            if math.fabs(w - lw) >= self._EPS:
                return False
        return True

    def _sample_ep(self):
        '''
        初始化样本分布的特征期望值
        :return:
        '''
        self._ep_ = [0.0] * self._n
        for i, xy in enumerate(self._numXY):
            self._ep_[i] = self._numXY[xy] * 1.0 / self._N
            self._xyID[xy] = i

    def _zx(self, X):
        '''
        计算Z(x)
        :param X: 特征+标签
        :return:
        '''
        # calculate Z(x)
        ZX = 0.0
        for y in self._Y:  # 对于每一个标签
            sum = 0.0
            for x in X:
                if (x, y) in self._numXY:  # 如果训练数据中存在这个特征
                    sum += self._w[self._xyID[(x, y)]]  # 特征的权值
            ZX += math.exp(sum)
        return ZX

    def _pyx(self, X):
        '''
        计算P(y|x)
        :param X: 输入的特征+标签
        :return:
        '''
        ZX = self._zx(X)
        results = []
        for y in self._Y:
            sum = 0.0
            for x in X:
                if (x, y) in self._numXY:
                    sum += self._w[self._xyID[(x, y)]]
            pyx = 1.0 / ZX * math.exp(sum)
            results.append((y, pyx))  # 标签-概率
        return results

    def _model_ep(self):
        '''
        计算模型期望
        :return:
        '''
        self._ep = [0.0] * self._n
        for sample in self._samples:
            X = sample[1:]
            pyx = self._pyx(X)
            for y, p in pyx:
                for x in X:
                    if (x, y) in self._numXY:
                        self._ep[self._xyID[(x, y)]] += p * 1.0 / self._N

    def train(self, maxiter=100):
        '''
        训练模型
        :param maxiter: 迭代次数可调，这里设置为100次
        :return:
        '''
        self._initparams()
        for i in range(0, maxiter):
            print("Iter:%d...." % i)
            self._lastw = self._w[:]  # 保存上一轮权值
            self._model_ep()
            # 更新每个特征的权值
            for i, w in enumerate(self._w):
                self._w[i] += 1.0 / self._C * math.log(self._ep_[i] / self._ep[i])
            print(self._w)
            # 检查是否收敛
            if self._convergence():
                break

    def predictSentence(self, inp):
        '''
        预测，支持句子输入
        :param inp: 输入句子
        :return:
        '''
        X = inp.strip().split("\t")
        prob = self._pyx(X)
        return prob

    def predictFile(self, testfile, resultfile):
        '''
        预测，支持文件输入
        :param testfile: 测试文件
        :param resultfile: 测试结果文件
        :return:
        '''
        infile = open(testfile, 'r', encoding="utf-8")
        outfile = open(resultfile, 'w', encoding="utf-8")
        for line in infile.readlines():
            prob = self.predictSentence(line)
            result = sorted(prob, key=lambda x: (x[1], x[0]), reverse=True)
            outfile.write(line.strip().split('\t')[0] + '\t' + result[0][0] + '\n')
        infile.close()
        outfile.close()

    def saveModel(self):
        '''
        将中间数据存入模型文件
        :param modelFile:
        :return:
        '''

        with open('model.pickle', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump(
                [self._samples, self._Y, self._numXY, self._N, self._n, self._xyID, self._C, self._ep_, self._ep,
                 self._w, self._lastw, self._EPS], f)
        f.close()

    def loadModel(self):
        '''
        加载模型文件
        :return: 
        '''
        with open('model.pickle', 'rb') as f:
            self._samples, self._Y, self._numXY, self._N, self._n, self._xyID, self._C, self._ep_, self._ep, self._w, self._lastw, self._EPS = pickle.load(
                f)
        # print(self._samples, self._Y, self._numXY, self._N, self._n, self._xyID, self._C, self._ep_, self._ep,
        #       self._w, self._lastw, self._EPS)
        f.close()


if __name__ == "__main__":
    time_start = time.time()
    maxent = MaxEnt()
    # maxent.load_data('data/trainFeature.txt')
    # maxent.train()
    # maxent.saveModel()
    maxent.loadModel()
    maxent.predictFile('data/testFeature.txt', 'result.txt')

    time_end = time.time()
    print('totally cost', time_end - time_start)
    # print(maxent.predictSentence("藏	    们	收	北	京	收/藏	藏/北	们/收/藏	藏/北/京	们/收/藏/北/京"))
    # print(maxent.predictSentence("北	    收	藏	京	史	藏/北	北/京	收/藏/北	北/京/史	收/藏/北/京/史"))
    # print(maxent.predictSentence("京	    藏	北	史	料	北/京	京/史	藏/北/京	京/史/料	藏/北/京/史/料"))
    # print(maxent.predictSentence("史	    北	京	料	中	京/史	史/料	北/京/史	史/料/中	北/京/史/料/中"))


    sys.exit(0)
