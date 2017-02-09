#!/usr/bin/env python
#coding=utf-8

import os
import sys
import jieba
import jieba.posseg as posseg

from replace_dict import pattern_dict
from multiprocessing import Pool

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

def replace_str(input_list, pattern_dict):
    new_list = [pattern_dict[x] if x in pattern_dict else x for x in input_list]
    return new_list

def get_allnoun(content):
    #Decode the text data to ascii
    content = content.decode('utf8')
    word_list = posseg.cut(content)
    allnoun_list = []
    for w in word_list:
        if 'n' in w.flag:
            allnoun_list.append(w.word)
    return allnoun_list

def get_file_list(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            path = os.path.join(root, file_name)
            file_list.append(path)
    return file_list

def get_chem_noun(file_path, pattern_dict=pattern_dict, keywords_list=keywords_list):
    content = file(file_path).read()
    all_noun = get_allnoun(content)
    all_noun_rep = replace_str(all_noun, pattern_dict)
    chemnoun_list = list(set(all_noun_rep) & set(keywords_list))
    if chemnoun_list:
        chemnouns = ' -- '.join(chemnoun_list) + ';\n'
        return chemnouns

def save_as_dot_file(root, year, chemnoun_list):
    filename = "result-" + year + ".dot"
    path = os.path.join(root, filename)
    file_head = "graph {\n"
    file_end = "}"
    with open(path, "w") as f:
        f.write(file_head)
        f.writelines(chemnoun_list)
        f.write(file_end)
    return True

reload(sys)
sys.setdefaultencoding('utf-8')

# Load userdict into jieba
jieba.load_userdict(user_dict)

# We put one years's data into one file
# And we make it compatible with Graphwiz's dot file
# We use multithreading to speed up the work
# set num in the Pool() 
# the num equal to the num of logical core the CPU have
p = Pool(4)
for year in os.listdir(source_dir):
    source_path = os.path.join(source_dir, year)
    file_list = get_file_list(source_path)
    chemnoun_list = p.map(get_chem_noun, file_list)
    chemnoun_list = [str(l) for l in chemnoun_list if l]
    save_as_dot_file(result_dir, year, chemnoun_list)
