#!/usr/bin/env python
# coding:utf-8

import os
import os.path
import sys
import jieba

# Set the Default coding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Define where we put the files:
source_dictionary = "/data/paper/guokr_data/2012/"
keywords_file = "/data/paper/keywords/keywords.txt"
result_file = "/data/paper/result-guokr-2012.txt"
user_dict = "/data/paper/keywords/user_dict.txt"

jieba.load_userdict(user_dict)

# Convert the Keywords file into a list
keywords_list = []
f = file(keywords_file)

while True:
    line = f.readline().strip().decode('utf-8')
    if len(line) == 0:
        break
    keywords_list.append(line)


r = open(result_file, "w")
# Get all the txt files in the dictionary
for root, dirs, files in os.walk(source_dictionary):
    for file_name in files:
        source_file = os.path.join(root, file_name)
        source_article = open(source_file).read().decode('utf-8')
        words_list = list(jieba.cut(source_article, cut_all=False))
        result = list(set(words_list) & set(keywords_list))
        if result:
            #r.write("The Title of the Content is %s :" % file_name)
            #r.write("\n")
            r.write(';'.join(result))
            r.write("\n")
r.close()
