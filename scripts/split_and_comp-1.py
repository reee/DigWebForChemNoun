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

text = "支持中國大陸.灣。香港！異體字和地區習慣用詞轉換"
result = ";".join(split_to_sentence(text))
print result
