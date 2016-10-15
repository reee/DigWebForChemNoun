#!/usr/bin/env python
#coding=utf-8

import os
import sys
import jieba
import jieba.posseg as posseg
import chardet


from langconv import *

def get_allnoun(content):
    #Decode the text data to ascii
    content = content.decode('utf8')
    #Convert chinese traditional to chinese simplified
    content = Converter('zh-hans').convert(content)
    word_list = posseg.cut(content)
    allnoun_list = []
    for w in word_list:
        if 'n' in w.flag:
            allnoun_list.append(w.word)
    return allnoun_list

reload(sys)
sys.setdefaultencoding('utf-8')

# Define which site we are dealing with By ourself!:
site_name = raw_input('Please Input the site name: ')

# Define where we put the files:
source_dir = "/data/site_data/" + site_name
user_dict = "/data/paper/keywords/user_dict.txt"
result_dir = "/data/paper/result/" + site_name
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# Load userdict into jieba
jieba.load_userdict(user_dict)

# We put one years's data into one file
# And we make it compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + '/' + year + '/'
    result_by_year = result_dir + '/result-allnoun-' + site_name + '-' + year + '.dot'
    f = open(result_by_year, "w")
    file_head = "graph " + site_name + "-" + year + " {" + "\n"
    file_end = "}"
    f.write(file_head)
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            content = file(source_file).read()
            result = get_allnoun(content)
            if result:
                result = ' -- '.join(result) + ';' + '\n'
                f.write(result)
    f.write(file_end)
    f.close()
