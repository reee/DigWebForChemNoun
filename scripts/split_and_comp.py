#!/usr/bin/env python
# coding:utf-8

import os
import os.path
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
keywords_list = []
f = file(keywords_file)
while True:
    line = f.readline().strip().decode('utf-8')
    if len(line) == 0:
        break
    keywords_list.append(line)

#We put all the result in a delicated file for review:
r = open(result_file, "a")
# We put one years's data into one file
# And it is compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + "/" + year + "/"
    result_year = result_dir + "/result-" + site_name + "-" + year + ".dot"
    ry = open(result_year, "a")
    file_head = "graph " + site_name + "-" + year + " {" + "\n"
    file_root = "}"
    ry.write(file_head)
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            source_article = open(source_file).read().decode('utf-8')
            words_list = list(jieba.cut(source_article, cut_all=False))
            result = list(set(words_list) & set(keywords_list))
            # If the result is not empty, put into the file:
            if result:
                ry.write(' -- '.join(result))
                ry.write(";")
                ry.write("\n")
                # We need to know where are the keywords from:
                r.write("The Title of the Content is %s :" % file_name)
                r.write("\n")
                r.write(';'.join(result))
                r.write("\n")
    ry.write(file_root)
    ry.close()
r.close()
