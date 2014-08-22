#!/usr/bin/env python
# coding:utf-8

import os
import sys
import jieba

#Set the Default coding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Define where we put the  files
source_dictionary = "/opt/ht/txt-add/"
keywords_file = "/opt/ht/keywords.txt"
result_file = "/opt/ht/result-add.txt"

# Convert the Keywords into a list
keywords_list = []
f = file(keywords_file)

while True:
    line = f.readline().strip().decode('utf-8')
    if len(line) == 0:
        break
    keywords_list.append(line)

# Deal With the source file
file_list = os.listdir(source_dictionary)

r_file = open(result_file, "w")

for files in file_list:
    r_file.write("------The file name We Deal With is %s ------" % files)
    r_file.write('\n')
    s_article = open(source_dictionary + files).read().decode('utf-8')
    s_sentence = s_article.split(u"。")
    for sentences in s_sentence:
        words_list = list(jieba.cut(sentences,cut_all=False))
        result = list(set(words_list) & set(keywords_list))
        r_file.write(';'.join(result))
        r_file.write('\n')
    r_file.write("--------File End---------")
    r_file.write('\n')
r_file.close()
