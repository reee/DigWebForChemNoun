#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

# generate the url_list
from dateutil.rrule import *
from datetime import *
date_list = list(rrule(DAILY, dtstart=datetime(2011,8,16), \
            until=datetime.today()))
date_list = [str(date) for date in date_list]
url_list = []
for date in date_list:
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    url = "http://www.cankaoxiaoxi.com/history/index/" + year + "-" + month \
        + "/" + day + "-00.shtml"
    url_list.append(url)

# Define the site we are going to crawl
site_name = "ckxx"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class zqbSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "cankaoxiaoxi.com",
    ]
    start_urls = url_list
    
    rules = (
        Rule(LinkExtractor(allow=('/\d{4}/\d{4}/\S*\.shtml')), callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/history/index/\d{4}-\d{2}/\d{2}-\d{2}\.shtml')), follow=True)
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        year = response.url.split('/')[3]
        month = response.url.split('/')[4][0:2]
        path = data_dir + '/' + year + '/' + month 
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        if response.xpath('//h1/text()').extract():
            title = response.xpath('//h1/text()').extract()[0]
        else:
            title = response.xpath('//h2/text()').extract()[0]
        # get the content
        content_list = response.xpath('//div[@id="ctrlfscont"]//p/text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
