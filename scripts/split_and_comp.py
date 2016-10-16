#!/usr/bin/env python
#coding=utf-8

import os
import sys
import jieba
import jieba.posseg as posseg
import opencc

from replace_dict import pattern_dict

def replace_str(input_list, pattern_dict):
    new_list = [pattern_dict[x] if x in pattern_dict else x for x in input_list]
    return new_list

def get_allnoun(content):
    #Decode the text data to ascii
    content = content.decode('utf8')
    #Convert chinese traditional to chinese simplified
    # content = opencc.convert(content, config='t2s.json')
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
keywords_file = "/data/paper/keywords/keywords.txt"
user_dict = "/data/paper/keywords/user_dict.txt"
result_dir = "/data/paper/result/" + site_name
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# Convert the Keywords file into a list
keywords_list = open(keywords_file).readlines()
keywords_list = [key.decode('utf-8').strip() for key in keywords_list]

# Load userdict into jieba
jieba.load_userdict(user_dict)

# We put one years's data into one file
# And we make it compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + '/' + year + '/'
    result_by_year = result_dir + '/result-' + site_name + '-' + year + '.dot'
    f = open(result_by_year, "w")
    file_head = "graph {\n"
    file_end = "}"
    chemnouns_list = []
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            content = file(source_file).read()
            allnoun_list = get_allnoun(content)
            allnoun_list_rep = replace_str(allnoun_list, pattern_dict)
            chemnoun_list = list(set(allnoun_list_rep) & set(keywords_list))
            if chemnoun_list:
                chemnouns = ' -- '.join(chemnoun_list) + ';\n'
                chemnouns_list.append(chemnouns)
    f.write(file_head)
    f.writelines(chemnouns_list)
    f.write(file_end)
    f.close()
