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
date_list = list(rrule(DAILY, dtstart=datetime(2007,12,16), \
            until=datetime.today()))
date_list = [str(date) for date in date_list]
url_list = []
for date in date_list:
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    url = "http://cqrbepaper.cqnews.net/cqrb/html/" + year + "-" + month \
        + "/" + day + "/node_124.htm"
    url_list.append(url)

# Define the site we are going to crawl
site_name = "cqrb"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class cqrbSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "cqrbepaper.cqnews.net",
    ]
    start_urls = url_list

    rules = (
        Rule(LinkExtractor(allow=('/cqrb/html/\d{4}-\d{2}/\d{2}/content.+$')), \
        callback='parse_data', follow=True,),
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = response.url.split('/')[5]
        year = time[0:4]
        month = time[5:7]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('//tr/td/strong/text()').extract()[1].strip().encode('utf-8')
        # get the content
        content_list = response.xpath('//*[@id="ozoom"]/founder-content//text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
