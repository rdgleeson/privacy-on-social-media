#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 13:27:09 2018

@author: rgleeson
"""

def main():
    file = open("filmratingslanguage.csv", "r")
    count = 0
    privatewords = {}
    publicwords = {}
    for line in file:
        if count == 0:
            count = 1
            continue
        else:
            line = line.strip()
            line = line.split(",")
            word = line[0]
            private = line[2]
            public = line [4]
            private = int(private.split("%")[0])
            public = int(public.split("%")[0])
            if private > 0:
                privatewords[word] = private
            if public > 0:
                publicwords[word] = public
    file.close()
    
    file = open("private.txt", "w")
    for key in privatewords.keys():
        for i in range(0, privatewords[key]):
            file.write(key)
            file.write(" ")
    file.close()
    
    file = open("public.txt", "w")
    for key in publicwords.keys():
        for i in range(0, publicwords[key]):
            file.write(key)
            file.write(" ")
    file.close()
main()
            
            