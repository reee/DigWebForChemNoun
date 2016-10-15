#!/usr/bin/env python
#coding=utf-8

from replace_dict import pattern_dict

def replace_str(input_list, pattern_dict):
    new_list = [pattern_dict[x] if x in pattern_dict else x for x in input_list]
    return new_list

list1 = ["黄金", "醋酸"]
newlist = replace_str(list1, pattern_dict)
print pattern_dict["醋酸"]
print ";".join(newlist)
