#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os
import uuid
from boilerpipe.extract import Extractor

# generate the url_list
from dateutil.rrule import *
from datetime import *
date_list = list(rrule(DAILY, dtstart=datetime(2015,01,01), \
            until=datetime.today()))
date_list = [str(date) for date in date_list]
url_list = []
for date in date_list:
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    url = "http://paper.people.com.cn/rmrb/html/" + year + "-" + month + "/" + day + "/nbs.D110000renmrb_01.htm"
    url_list.append(url)

# Define the site we are going to crawl
site_name = "rmrb"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class cqrbSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "paper.people.com.cn",
    ]
    start_urls = url_list

    rules = (
        Rule(LinkExtractor(allow=('/rmrb/html/\d{4}-\d{2}/\d{2}/nw.+$')), \
        callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/rmrb/html/20\d{2}-\d{2}/\d{2}/nbs.+$')), follow=True),
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = response.url.split('/')[5]
        year = time[0:4]
        month = time[5:7]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        content = extractor.getText().encode('utf-8')

        filename = path + '/' + str(uuid.uuid4()) + '.txt'
        with open(filename, 'wb') as f:
            f.write(content)
