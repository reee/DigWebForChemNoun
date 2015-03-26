#coding=utf-8

import os
import sys
import jieba

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

def get_chemnoun(word_list, key_list):
    chemnoun_list = []
    for word in word_list:
        word = word.strip()
        for key in key_list:
            key = key.strip()
            if key in word:
                chemnoun_list.append(word)
                break
    return chemnoun_list

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

# load the keywords file as a list
f = file(keywords_file).decode('utf-8')
key_list = f.readlines()
f.close()

# We put one years's data into one file
# And we make it compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + '/' + year + '/'
    result_year = result_dir + '/result-' + site_name + '-' + year + '.dot'
    ry = open(result_year, "a")
    file_head = "graph " + site_name + "-" + year + " {" + "\n"
    file_root = "}"
    ry.write(file_head)
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            source_article = open(source_file).read().decode('utf-8')
            # ry.write("The Title of the Content is %s : \n" % file_name)
            sentence_list = split_to_sentence(source_article)
                for sentence in sentence_list:
                    words_list = list(jieba.cut(sentence, cut_all=False))
                    result = get_chemnoun(words_list, key_list)
                    if result:
                        result = ' -- '.join(result) + ';' + '\n'
                        ry.writelines(result)
                        r.writelines(result)
    ry.write(file_root)
    ry.close()
