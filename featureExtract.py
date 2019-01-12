#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : featureExtract.py
@Time : 2018/12/11 13:45
@Site : 
@Software: PyCharm
'''
'''
对训练文件和测试文件提取特征
'''
# inFileGenia = open('data/test_data', 'r', encoding="utf-8")
# oFileTrain = open('data/testfeature.txt', 'w', encoding="utf-8")

inFileGenia = open('data/train_data', 'r', encoding="utf-8")
oFileTrain = open('data/trainFeature.txt', 'w', encoding="utf-8")

sentenceList = []  # initialize sentence list
tag = []
IOBList = []  # initialize entity list
tempList = []  # initialize templist to append features for current token, this list gets dumped after each token is written to file
numSentences = 0  # counter for num of sentences processed
counter=0
dic = {'B-ORG', 'I-ORG', 'B-PER', 'I-PER', 'B-LOC', 'I-LOC'}
for line in inFileGenia:
    # split the current token and entity and load into initial list
    inputTokenEntity = line.split()
    # if numSentences >= 50:
    #     break
    # statement determines whether end of sentence or not.  If not end of sentence, then keep getting tokens to build sentence
    # once sentence is built, then do processing to create feature set for each token
    if len(inputTokenEntity) == 0:
        for item in IOBList:
            if item in dic:
                counter=counter+1
                break
        i = 0
        for token in sentenceList:
            # append IOBs
            tempList.append(IOBList[i])
            # append token and POSTags
            tempList.append(token)
            # tempList.append(tag[sentenceList.index(token)])

            if i == 0 and len(IOBList) > 2:
                tempList.append('0')
                # tempList.append('0')
                tempList.append('0')
                # tempList.append('0')
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append(sentenceList[i + 2])
                # tempList.append(tag[i + 2])

            if i == len(IOBList) - 1 and len(IOBList) > 2:
                tempList.append(sentenceList[i - 2])
                # tempList.append(tag[i - 2])
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append('0')
                # tempList.append('0')
                tempList.append('0')
                # tempList.append('0')

            if i == 1 and len(IOBList) > 3:
                tempList.append('0')
                # tempList.append('0')
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append(sentenceList[i + 2])
                # tempList.append(tag[i + 2])

            if i == len(IOBList) - 2:
                tempList.append(sentenceList[i - 2])
                # tempList.append(tag[i - 2])
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append('0')
                # tempList.append('0')

            if i >= 2 and i < len(IOBList) - 2:
                tempList.append(sentenceList[i - 2])
                # tempList.append(tag[i - 2])
                tempList.append(sentenceList[i - 1])
                # tempList.append(tag[i - 1])
                tempList.append(sentenceList[i + 1])
                # tempList.append(tag[i + 1])
                tempList.append(sentenceList[i + 2])
                # tempList.append(tag[i + 2])

            # 前一个词与当前词
            if i > 0:
                tempList.append(sentenceList[i - 1] + '/' + token)
            else:
                tempList.append('0')
            # 当前词与后一个词
            if i < len(IOBList) - 1:
                tempList.append(token + '/' + sentenceList[i + 1])
            else:
                tempList.append('0')
            # 当前词与前两个词
            if i > 1:
                tempList.append(sentenceList[i - 2] + '/' + sentenceList[i - 1] + '/' + token)
            else:
                tempList.append('0')

            # 当前词与后两个词
            if i < len(IOBList) - 2:
                tempList.append(token + '/' + sentenceList[i + 1] + '/' + sentenceList[i + 2])
            else:
                tempList.append('0')

            # 当前词与前后两个词
            if i > 1 and i < len(IOBList) - 2:
                tempList.append(
                    sentenceList[i - 2] + '/' + sentenceList[i - 1] + '/' + token + '/' + sentenceList[i + 1] + '/' +
                    sentenceList[i + 2])
            else:
                tempList.append('0')

            # 词形特征
            # orgDic = {'部', '院', '社', '中央'}
            # flag1 = 0
            # for item in orgDic:
            #     if item in token:
            #         tempList.append('org')
            #         flag1 = 1
            #         break
            # if flag1 == 0:
            #     tempList.append('0')
            #
            # # 边界特征
            # leftDic = {'记者', '主席', '总理', '总统', '部长', '书记', '主任', '了'}
            # rightDic = {'说', '同志', '报道', '等', '摄', '主席'}
            # if i == 0 or i == len(IOBList) - 1:
            #     tempList.append('0')
            # elif sentenceList[i - 1] in leftDic :
            #     tempList.append('b-per')
            # elif sentenceList[i + 1] in rightDic:
            #     tempList.append('i-per')
            # else:
            #     tempList.append('0')

            # write out token and features to file
            for item in tempList[:-1]:
                oFileTrain.write("%s\t" % item)
            oFileTrain.write("%s" % tempList[-1])
            oFileTrain.write("\n")

            # clear out tempList and increment current token
            tempList = []
            i = i + 1

        oFileTrain.write("\n")
        sentenceList = []
        tag = []
        IOBList = []

        # increment number of sentences processed and print to screen
        numSentences = numSentences + 1
        print(numSentences)

    else:
        # not end of sentence, so continue to build arrays
        sentenceList.append(inputTokenEntity[0])
        # tag.append(inputTokenEntity[1])
        IOBList.append(inputTokenEntity[1])

print("Feature Extraction Complete")
print(counter)