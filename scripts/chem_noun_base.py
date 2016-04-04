#!/usr/bin/env python
#coding=utf-8

import os
import sys
import jieba
import jieba.posseg as posseg
import chardet

from chardet.universaldetector import UniversalDetector
from langconv import *


def split_to_sentence(content):
    #Decode the text data to ascii
    content = content.decode('utf8')
    #Convert chinese traditional to chinese simplified
    content = Converter('zh-hans').convert(content)
    # Init the MAGIC!
    start = 0
    i = 0
    sentence_list = []
    punct_list = ',.!?:;~，。！？：；～'.decode('utf8')
    for word in content:
        if word in punct_list:
            sentence_list.append(content[start:i+1])
            start = i + 1
            i += 1
        else:
            i += 1

    if start < len(content):
        sentence_list.append(content[start:])
    return sentence_list

def conv_to_list(input_file):
    with open(input_file) as f:
        content = f.readlines()
        detector = UniversalDetector()
        for line in content:
            detector.feed(line)
            if detector.done: break
        detector.close()
        content_codec = detector.result['encoding']
        content_decoded = [line.decode(content_codec).strip() for line in content]
    return content_decoded

# We think that paragraph is definded by 'Carriage return'. 
# So split a file into paragraph is equal to convert the file into a list by 'LINE'
def split_to_para(input_file):
    return conv_to_list(input_file)

def get_all_noun(input_content, blacklist=None):
    word_list = posseg.cut(input_content)
    noun_list = []
    for w in word_list:
        if 'n' in w.flag:
            if blacklist and not (w.word in blacklist):
                noun_list.append(w.word)
            else:
                noun_list.append(w.word)
    return noun_list
            
def get_chemnoun_simple(input_content, key_list):
    words_list = list(jieba.cut(source_article, cut_all=False))
    chemnoun_list = list(set(words_list) & set(key_list))
    return chemnoun_list

def get_chemnoun(input_content, key_list, blacklist):
    word_list = posseg.cut(input_content)
    chemnoun_list = []
    key_set = set(key_list)
    for w in word_list:
        # n in flag means it's noun
        if 'n' in w.flag:
            if (w.word in key_set) and not (w.word in blacklist):
                chemnoun_list.append(w.word)
    return chemnoun_list

def get_chemnoun_by_para(input_file, key_list, blacklist):
    para_list = split_to_para(input_file)
    chemnoun_list = []
    for para in para_list:
        chemnouns = get_chemnoun(para, key_list, blacklist)
        if chemnouns:
            chemnoun_list.append(chemnouns)
    return chemnoun_list

def get_chemnoun_by_sentence(input_file, key_list, blacklist):
    sentence_list = split_to_sentence(input_file)
    chemnoun_list = []
    for sentence in sentence_list:
        chemnouns = get_chemnoun(sentence, key_list, blacklist)
        if chemnouns:
            chemnoun_list.append(chemnouns)
    return chemnoun_list
