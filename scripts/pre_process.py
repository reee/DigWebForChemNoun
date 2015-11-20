#encoding=utf-8

keywords_file = "/data/paper/keywords/keywords.txt"
added_not_chemnoun = "/data/paper/keywords/added_not_chemnoun.txt"
dict_file = "/data/paper/keywords/user_dict.txt"

import sys

#Set the Default codingg to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

def conv_to_user_dict(keyword):
    word_weight = len(keyword) * 10
    user_dict =  keyword + " " + str(word_weight) + " n"
    return user_dict

keywords_list = open(keywords_file).readlines()
not_chem_list = open(added_not_chemnoun).readlines()

keywords_list = sorted(list(set(keywords_list)))
not_chem_list = sorted(list(set(not_chem_list)))

word_list = keywords_list + not_chem_list
word_list = [word.strip().decode('utf-8') for word in word_list]
dict_list = [conv_to_user_dict(word) for word in word_list]

with open(dict_file, 'w') as d:
    d.write("\n".join(dict_list))

with open(keywords_file, 'w') as k:
    k.write("".join(keywords_list))

with open(added_not_chemnoun, 'w') as a:
    a.write("".join(not_chem_list))
