#!/usr/bin/env python
#coding=utf-8

result_dir = "/data/paper/result"

import os
from collections import Counter

sites = os.listdir(result_dir)
for site in sites:
    site_dir = os.path.join(result_dir, site)
    all_files = os.listdir(site_dir)
    files = [f for f in all_files if f.endswith('dot')]
    for f in files:
        input_path = os.path.join(site_dir, f)
        year = f.split(".")[0].split("-")[1]
        output_filename = "state-" + year + ".txt"
        output_path = os.path.join(site_dir, output_filename)
        output_content = []
        with open(input_path) as s:
            l = list(s)[1:-1]
            l = [line.strip(";\n").split(" -- ") for line in l]
            l = [x for j in l for x in j]
            c = Counter(l)
            count_all = sum(c.values())
            output_content.append("Total Word is %s \n" % count_all)
            output_content.append("Word,Percent,Count \n")
            top_50 = c.most_common(50)
            for i in top_50:
                word = i[0]
                count = i[1]
                percent = str(round(float(count)/float(count_all), 4))
                output_content.append("%s,%s,%s \n" % (word, percent, count))
            with open(output_path, 'w') as o:
                o.truncate()
                o.writelines(output_content)


