#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "songshuhui"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

class SongshuhuiSpider(CrawlSpider):
    name = site_name
    allowed_domains = ["songshuhui.net"]
    start_urls = [
        "http://songshuhui.net",
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/archives/\d+$')), callback='parse_data', follow=True,),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = response.xpath('//div[@class="metax_single"]/text()').extract()[0].strip()
        year = time[4:8]
        month = time[9:11]
        path = data_dir + '/' + year + '/' + month 
        if not os.path.exists(path):
            os.makedirs(path)
        # get the title
        title = response.xpath('//span[@class="contenttitle"]//text()').extract()[1].strip()
        # get the content
        content_list = response.xpath('//div[@class="entry"]//text()').extract()
        content = "".join(content_list).strip().encode("utf8")

        filename = path + '/' +  title + '.txt'
        with open(filename, 'wb') as f:
                f.write(content)
