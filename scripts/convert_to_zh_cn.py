#coding=utf-8

from langconv import *

r = file('/data/paper/keywords/keywords-checked.txt', 'r')
rr = file('/data/paper/keywords/keywords-1.txt', 'w')
content = r.read().decode('utf8')
content = Converter('zh-hans').convert(content)
content = content.encode('utf8')
rr.write(content)
r.close()
rr.close()
