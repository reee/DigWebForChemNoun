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
date_list = list(rrule(DAILY, dtstart=datetime(2010,11,26), \
            until=datetime.today()))
date_list = [str(date) for date in date_list]
url_list = []
for date in date_list:
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    url = "http://zqb.cyol.com/html/" + year + "-" + month \
        + "/" + day + "/nbs.D110000zgqnb_01.htm"
    url_list.append(url)

# Define the site we are going to crawl
site_name = "zqb"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

# We should rename the Spider's Class
class zqbSpider(CrawlSpider):
    name = site_name
    allowed_domains = [
        "zqb.cyol.com",
    ]
    start_urls = url_list

    rules = (
        Rule(LinkExtractor(allow=('/html/\d{4}-\d{2}/\d{2}/nw\.D110000zgqnb_\d{8}_\d{1,2}-\d{1,2}\.htm')), \
        callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/html/\d{4}-\d{2}/\d{2}/nbs\.D110000zgqnb_\d{2}.htm')), \
        follow=True,),
    )

    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time = response.url.split('/')[4]
        year = time[0:4]
        month = time[5:7]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        # Get the title
        title = response.xpath('/html/body/div[3]/div[2]/div[5]/div/h1/text()').extract()[0].strip().encode('utf-8')
        # get the content
        content_list = response.xpath('//*[@id="ozoom"]//p/text()').extract()
        content = "".join(content_list).strip().encode("utf-8")
        # If the time or the content is empty,Means we get the wrong page
        # Do not create the file
        if title and content:
            filename = path + '/' +  title + '.txt'
            with open(filename, 'wb') as f:
                f.write(content)
