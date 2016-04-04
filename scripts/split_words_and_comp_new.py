#!/usr/bin/env python
# coding:utf-8
#
# by <Zhang Hong>(zong777@gmail.com)

import os
import sys
import jieba
import chardet
from chardet.universaldetector import UniversalDetector
import jieba.posseg as posseg
from multiprocessing.dummy import Pool as ThreadPool


def split_to_sentence(input_file):
    with open(input_file) as f:
        content = f.read()
        content_codec = chardet.detect(content)['encoding']
        content = content.decode(content_codec)
        # Init the MAGIC!
        start = 0
        i = 0
        sentence_list = []
        punct_list = '.!?:;~，。！？：；～'.decode('utf8')
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

def get_chemnoun(input_content, key_list, blacklist):
    word_list = posseg.cut(input_content)
    chemnoun_list = []
    for w in word_list:
        # n in flag means it's noun
        if 'n' in w.flag:
            for key in key_list:
                if (key in w.word) and not (w.word in blacklist):
                    chemnoun_list.append(w.word)
                    break
    if chemnoun_list:
        chemnouns = ' -- '.join(chemnoun_list) + ';'
        return chemnouns


def get_chemnoun_by_para(input_file, key_list, blacklist):
    para_list = split_to_para(input_file)
    chemnoun_list = []
    for para in para_list:
        chemnouns = get_chemnoun(para, key_list, blacklist)
        if chemnouns:
            chemnoun_list.append(chemnouns)
    if chemnoun_list:
        title = "# 本文标题是 " + os.path.split(input_file)[1]
        chemnoun_list.insert(0, title)
        return chemnoun_list

def get_chemnoun_by_sentence(input_file, key_list, blacklist):
    sentence_list = split_to_sentence(input_file)
    chemnoun_list = []
    for sentence in sentence_list:
        chemnouns = get_chemnoun(sentence, key_list, blacklist)
        if chemnouns:
            chemnoun_list.append(chemnouns)
    if chemnoun_list:
        title = "# 本文标题是 " + os.path.split(input_file)[1]
        chemnoun_list.insert(0, title)
        return chemnoun_list

#Set the Default coding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Define where we put the files
data_base = "/data/site_data/"
keywords_file = "/data/paper/keywords/key.txt"
blacklist_file = "/data/paper/keywords/blacklist-ht.txt"
result_base = "/data/paper/result/"
user_dict = "/data/paper/keywords/user_dict.txt"

site_name = raw_input('Please Input the site name: ')
source_dir = os.path.join(data_base, site_name)
result_dir = os.path.join(result_base, site_name)

# Load userdict into jieba
jieba.load_userdict(user_dict)

# load the file as list
key_list = conv_to_list(key_file)
blacklist = conv_to_list(blacklist_file)

pool = ThreadPool(8)
result_list = []

# Do our JOB!
for year in os.listdir(source_dir):
    source_year = os.path.join(source_dir, year)
    result_name = site_name + '-' + year + '.dot'
    result_year = os.path.join(result_dir, result_name)
    y = open(result_year, "w")
    dot_head = "graph " + site_name + "-" + year + " {"
    dot_root = "}"
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        source_list = [os.path.join(root, file_name) for file_name in files]
        result_pool = pool.map(get_chemnoun_by_para, source_list)
        pool.close()
        pool.join()
        for result in result_pool:
            result_list += result
            result_list.insert(0, dot_head)
            result_list.append(dot_root)
            y.writelines(result_list)
    y.close()
