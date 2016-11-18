#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

# generate the url_list
# for cqrb the first available day is 2007,12,16
from dateutil.rrule import *
from datetime import *

date_list = list(rrule(DAILY, dtstart=datetime(2015,1,1), \
                    until=datetime.today()))
date_list = [d.strftime('%Y%m%d') for d in date_list]

url_list = []
for date in date_list:
    url = "http://www.solidot.org/?issue=" + date
    url_list.append(url)

# Define the site we are going to crawl
site_name = "solidot"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class solidotSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "solidot.org",
    ]
    start_urls = url_list
    
    rules = (
        Rule(LinkExtractor(allow=('story\?sid=\d+$')), \
        callback='parse_data', follow=True,),
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        date_string = response.xpath('//div[@class="talk_time"]/text()')\
        .extract()[2].split(' ')[2]
        year = date_string[0:4]
        month = date_string[5:7]
        path = data_dir + '/' + year + '/' + month 
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('//div[@class="bg_htit"]/h2/text()').extract()[0]
        # get the content
        content_list = response.xpath('//div[@class="p_mainnew"]/text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
