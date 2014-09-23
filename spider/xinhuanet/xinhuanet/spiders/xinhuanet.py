#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "xinhuanet"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name + '/'

# We should rename the Spider's Class
class XinHuaNetSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "news.xinhuanet.com",
    ]
    start_urls = [
        "http://www.xinhuanet.com",
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/\w+/\d{4}-\d{2}/\d{2}/\w+.htm')), callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/\w+/$')), follow=True,),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = response.url.split('/')[4]
        year = time[0:4]
        month = time[5:7]
        path = data_dir + year + '/' + month + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('//div[@class="main_tit"]/h1/text()').extract()[0].strip()
        # get the content
        content_list = response.xpath('//div[@id="content"]//text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
