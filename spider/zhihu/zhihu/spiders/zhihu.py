#coding=utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

base_dir = "/data/paper/zhihu_data"

class PeopleSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = [
        "www.zhihudaily.net",
    ]
    start_urls = [
        "http://www.zhihudaily.net/",
    ]

    rules = (
        Rule(LinkExtractor(allow=('/story/\d+/?$')), callback='parse_data', follow=True),
        Rule(LinkExtractor(allow=('/day/\d{8}/?$')), follow=True)
    )

    def parse_data(self, response):
        #Get the data 
        time_list = response.xpath('//a[@target="_self"]/@href').extract()
        time = ''.join(time_list)
        #Zhihu Has two Titles!
        q_title_list = response.xpath('//h2[@class="question-title"]/text()').extract()
        q_title = "".join(q_title_list).strip().encode('utf8')
        h_title_list = response.xpath('//h2[@class="headline-title"]/text()').extract()
        h_title = "".join(h_title_list).strip().encode('utf8')
        if h_title:
            title = h_title
        else:
            title = q_title
        
        content_list = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div/div/div[2]/text()').extract()
        content = "".join(content_list).strip().encode('utf8')
        
        #Store the file by year/month
        year = time[5:9].encode('utf8')
        month = time[9:11].encode('utf8')
        path = base_dir + '/' + year + '/' + month
        #If the dir does not exists, make it
        if not os.path.exists(path):
            os.makedirs(path)
        #If the time_list or the content_list is empty,Means we get the wrong page
        #Do not create the file
        if time_list and content_list and not title == "瞎扯 · 如何正确地吐槽":
            filename = path + '/' + title + '.txt'
            #filename = title + '.txt'
            with open(filename, "wb") as f:
                f.write(content)
