#coding=utf-8

import os
import sys
import jieba
import jieba.posseg as posseg
import chardet


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

def get_chemnoun(sentence, key_list, black_list):
    sentence = sentence.decode('utf-8')
    word_list = posseg.cut(sentence)
    chemnoun_list = []
    for w in word_list:
        if 'n' in w.flag:
            for key in key_list:
                key = key.decode('utf8').strip()
                if (key in w.word) and not (w.word in black_list) :
                    chemnoun_list.append(w.word)
                    break
    return chemnoun_list

reload(sys)
sys.setdefaultencoding('utf-8')

# Define which site we are dealing with By ourself!:
site_name = raw_input('Please Input the site name: ')

# Define where we put the files:
source_dir = "/data/site_data/" + site_name
keywords_file = "/data/paper/keywords/key.txt"
black_list_file = "/data/paper/keywords/blacklist.txt"
user_dict = "/data/paper/keywords/user_dict.txt"
result_dir = "/data/paper/result/" + site_name
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
result_file = result_dir + "/" + "result.txt"

# Load userdict into jieba
jieba.load_userdict(user_dict)

# load the keywords file as a list
f = file(keywords_file)
key_list = f.readlines()
f.close()

# Convert the blacklist file into a list
# And make sure convert it to unicode
black_list = []
f = file(black_list_file)
while True:
    line = f.readline().strip().decode('utf-8')
    if len(line) == 0:
        break
    black_list.append(line)

# We put one years's data into one file
# And we make it compatible with Graphwiz's dot file
for year in os.listdir(source_dir):
    source_year = source_dir + '/' + year + '/'
    result_year = result_dir + '/result-' + site_name + '-' + year + '.dot'
    y = open(result_year, "w")
    file_head = "graph " + site_name + "-" + year + " {" + "\n"
    file_root = "}"
    y.write(file_head)
    # Get all the txt files in the dictionary:
    for root, dirs, files in os.walk(source_year):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            para_list = open(source_file).readlines()
            y.write("# 本文标题是 %s : \n" % file_name)
            # sentence_list = split_to_sentence(source_article)
            # for sentence in sentence_list:
            for para in para_list:
                result = get_chemnoun(para, key_list, black_list)
                if result:
                    result = ' -- '.join(result) + ';' + '\n'
                    y.writelines(result)
    y.write(file_root)
    y.close()
