#encoding=utf-8
import jieba
import jieba.posseg as posseg

jieba.load_userdict("/data/paper/keywords/user_dict.txt")

words = posseg.cut("该组织报告中提到，三氯杀螨醇和硫丹都属于禁止用于茶树的农药", HMM=True)

for w in words:
        print('%s %s' % (w.word, w.flag))
