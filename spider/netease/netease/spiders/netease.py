#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "netease"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class NeteaseSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "news.163.com",
        "edu.163.com"
    ]
    start_urls = [
        "http://news.163.com",
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/1\d/\d{4}/\d{2}/.*\.html')), callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/\w+/$')), follow=True,),
        Rule(LinkExtractor(allow=('/\w+/\w+/.+\.html$')), follow=True,),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time1_list = response.xpath('//div[@class="ep-info cDGray"]/div[@class="left"]/text()').extract()
        time2_list = response.xpath('//span[@class="info"]/text()').extract()
        if time1_list:
            time = time1_list[0].strip()
        else:
            time = time2_list[0].strip()
        year = time[0:4]
        month = time[5:7]
        path = data_dir + '/' + year + '/' + month 
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('//h1[@id="h1title"]/text()').extract()[0]
        # get the content
        content_list = response.xpath('//div[@id="endText"]//text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
