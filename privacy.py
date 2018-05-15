#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 20:28:39 2018

@author: rgleeson
"""
#privacy.py

import StemmingUtil
import string
import sys
import math

class instance:
    def __init__(self, privacy):
        self.privacy = privacy
        self.wordProb = {} #keys are words, values are probabilities
        self.b = 0 #number of unique words equal to len(self.wordProb.keys())
        self.total = 0 #total words

class testInst:
    def __init__(self, privacy):
        self.privacy = privacy
        self.text = []

def processWords(text,stopWords):
    wl=[] #word list
    count=0
    for line in text:
        line = line.strip()
        line= ''.join(ch for ch in line if ch not in string.punctuation)
        line = line.split()
        for word in line:
            if count == 0:
                word = word.replace('\ufeff', '')
                count = 1
            word=word.lower()
            if word in stopWords:
                continue
            wl.append(word)
    stems = StemmingUtil.createStems(wl)
    return stems

def readBooks(line,stems,stopWords):
    book= open(line,"r",encoding="utf8")
    stems[line]=processWords(book,stopWords)
    book.close()
    return stems

def updateInstList(privacy, stems, Instances):
    inst = instance(privacy)
    for word in stems:
        if word in inst.wordProb.keys():
            inst.wordProb[word] += 1
        else:
            inst.wordProb[word] = 2
    inst.total = len(stems)
    inst.b = len(inst.wordProb.keys())
    Instances.append(inst)
    return Instances

def naiveBayes(test, trainingSet):
    label = test.privacy
    sumList = []
    b = 0
    unique = set()
    for inst in trainingSet:
        for word in inst.wordProb.keys():
            unique.add(word)
    b = len(unique)
    for inst in trainingSet:
        summ = math.log(1/9)
        for word in test.text:
            pci = 1
            if word in inst.wordProb.keys():
                pci = inst.wordProb[word]
            P = pci/(inst.total+b)    
            summ+= math.log(P)
        sumList.append((inst.privacy, summ))
    sumList.sort(key=lambda tup: tup[1], reverse = True)
    return (label, sumList[0][0])

def main():
    #creating the stopWords list
    stopWords = []
    #https://kb.yoast.com/kb/list-stop-words/
    SW = open("stop_words.txt", "r")
    for line in SW:
        line = line.lower()
        stopWords.append(line.strip())
    SW.close()
    
    #Reading in the books
    Instances = []
    trainingStems={}
    PostList= open("listofposts.txt","r")
    for line in PostList:
        line = line.strip() #e.g Austen_PridePrejudice_1342.txt
        trainingStems=readBooks(line,trainingStems,stopWords)
        lineList = line.split(".")
        privacy = lineList[0] #e.g Austen
        Instances = updateInstList(privacy, trainingStems[line], Instances)

    #Reading in the Facebook Passages
    FBInstances = [] 
    file = open("FacebookPosts.txt", "r",encoding="utf8")
    testStems={}
    for line in file:
        line = line.strip()
        line=''.join(ch for ch in line if ch not in string.punctuation)
        line=line.split()
               #get passage and process it  
        for word in line:
            wl = []
            word=word.lower()
            if word in stopWords:
                continue
            wl.append(word)
            testStems= StemmingUtil.createStems(wl) #returns stems of wl
        inst = testInst("blank")
        inst.text = testStems
        FBInstances.append(inst)
    file.close()
    
    #Reading in the Twitter Passages
    TWInstances = [] 
    file = open("TwitterPosts.txt", "r",encoding="utf8")
    testStems={}
    for line in file:
        line = line.strip()
        line=''.join(ch for ch in line if ch not in string.punctuation)
        line=line.split()
               #get passage and process it  
        for word in line:
            wl = []
            word=word.lower()
            if word in stopWords:
                continue
            wl.append(word)
            testStems= StemmingUtil.createStems(wl) #returns stems of wl
        inst = testInst("blank")
        inst.text = testStems
        TWInstances.append(inst)
    file.close()

    #run Naive Bayes on TestSet passages
    FBpred = {}
    for inst in FBInstances:
        tup = naiveBayes(inst, Instances)
        pred = tup[1]
        if pred in FBpred.keys():
            FBpred[pred] +=1
        else:
            FBpred[pred] = 1
    TWpred = {}
    for inst in TWInstances:
        tup = naiveBayes(inst, Instances)
        pred = tup[1]
        if pred in TWpred.keys():
            TWpred[pred] +=1
        else:
            TWpred[pred] =1
    print("Facebook:")
    for key in FBpred.keys():
        print("%s: %d" %(key, FBpred[key]), end="      ")
    print()
    print("Twitter:")
    for key in TWpred.keys():
        print("%s: %d" %(key, TWpred[key]), end="      ")
    
main()
    
