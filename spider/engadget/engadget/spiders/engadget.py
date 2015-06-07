#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

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
    start_urls = [
        "http://cn.engadget.com/"
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/\d{4}/\d{2}/\d{2}/.+/$')),callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/page/\d+/$')), follow=True)
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        year = response.url.split('/')[3]
        month = response.url.split('/')[4]
        path = data_dir + '/' + year + '/' + month 
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('//h1/text()').extract()[0].strip()
        # get the content
        content_list = response.xpath('//*[@id="body"]/div[1]/div[1]/div//text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
