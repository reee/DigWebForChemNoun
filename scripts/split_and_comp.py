#!/usr/bin/env python
# coding:utf-8

import os
import sys
import jieba

# Set the Default coding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Define which site we are dealing with By ourself!:
site_name = raw_input('Please Input the site name: ')

# Define where we put the files:
source_dir = "/data/site_data/" + site_name
keywords_file = "/data/paper/keywords/keywords.txt"
user_dict = "/data/paper/keywords/user_dict.txt"
result_dir = "/data/paper/result/" + site_name
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
result_file = result_dir + "/" + "result.txt"

# Load userdict into jieba
jieba.load_userdict(user_dict)

# Convert the Keywords file into a list
keywords_list = open(keywords_file).readlines()
keywords_list = [key.decode('utf-8').strip() for key in keywords_list]

# We put one years's data into one file
# And it is compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + "/" + year + "/"
    result_year = result_dir + "/result-" + site_name + "-" + year + ".dot"
    r = open(result_year, "a")
    file_head = "graph " + site_name + "-" + year + " {\n"
    file_root = "}"
    r.write(file_head)
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            source_article = open(source_file).read().decode('utf-8')
            words_list = list(jieba.cut(source_article, cut_all=False))
            result = list(set(words_list) & set(keywords_list))
            # If the result is not empty, put into the file:
            if result:
                #r.write("# 本文标题为：%s \n " % file_name)
                r.write(' -- '.join(result) + ";\n")
    r.write(file_root)
    r.close()
