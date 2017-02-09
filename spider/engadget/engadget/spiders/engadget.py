#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

import uuid
import re
from boilerpipe.extract import Extractor

# Define the site we are going to crawl
site_name = "engadget"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class engadgetSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "cn.engadget.com",
    ]
    site_url = "http://cn.engadget.com/page/"
    start_url1 = [site_url + str(i) + '/' for i in range(610,639)]
    start_url2 = [site_url + str(i) + '/' for i in range(641,1666)]
    start_urls = start_url1 + start_url2

    rules = (
        Rule(LinkExtractor(allow=('/\d{4}/\d{2}/\d{2}/(\w+-?)+/$')),callback='parse_data'),
        Rule(LinkExtractor(allow=('/page/(\d|\d{2}|\d{3}|2\d{3})/$')), follow=True)
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = re.findall("/\d{4}/\d{2}/\d{2}/", response.url)[0]
        year = time[1:5]
        month = time[6:8]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        content = extractor.getText().encode('utf-8')
        if content:
            filename = path + '/' + str(uuid.uuid4()) + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)

