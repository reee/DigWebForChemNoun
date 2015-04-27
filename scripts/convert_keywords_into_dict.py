#encoding=utf-8

import sys

def conv_to_user_dict(keyword):
    word_weight = len(keyword) * 10
    return keyword + " " + str(word_weight) + " n"

#Set the Default codingg to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

keywords_file = "/data/paper/keywords/keywords.txt"
added_not_chemnoun = "/data/paper/keywords/added_not_chemnoun.txt"
dict_file = "/data/paper/keywords/user_dict.txt"

k = open(keywords_file).readlines()
a = open(added_not_chemnoun).readlines()

word_list = k + a
word_list = [word.strip().decode('utf-8') for word in word_list]
dict_list = [conv_to_user_dict(word) for word in word_list]
with open(dict_file, 'w') as d:
    d.write("\n".join(dict_list))

