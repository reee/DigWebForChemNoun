#encoding=utf-8

import sys

#Set the Default codingg to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

keywords_file = "/data/paper/keywords/keywords-checked.txt"
dict_file = "/data/paper/keywords/user_dict.txt"

dict_list = []
f = file(keywords_file)

while True:
    line = f.readline().strip().decode('utf-8')
    if len(line) == 0:
        break
    word_weight = len(line) * 10
    dict_line = line + " " + str(word_weight) + " " + "n"
    dict_list.append(dict_line)

d = open(dict_file, "w")
dict_content = "\n".join(dict_list)
d.write(dict_content)
d.close

