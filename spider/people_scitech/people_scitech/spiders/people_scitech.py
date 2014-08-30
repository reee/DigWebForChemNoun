from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

base_dir = "/data/paper/people_data"

class PeopleSpider(CrawlSpider):
    name = "people"
    allowed_domains = [
        "scitech.people.com.cn",
        "health.people.com.cn",
    ]
    start_urls = [
        "http://scitech.people.com.cn",
        "http://health.people.com.cn",
    ]

    rules = (
        Rule(LinkExtractor(allow=('/n/\d+/\d+/.+\.html$')), callback='parse_data', follow=True),
        Rule(LinkExtractor(allow=('/GB/.+\.html')), follow=True)
    )

    def parse_data(self, response):
        #Get the data 
        time_list = response.xpath('//span[@id="p_publishtime"]/text()').extract()
        time = ''.join(time_list)
        title_list = response.xpath('//h1[@id="p_title"]/text()').extract()
        title = "".join(title_list).strip().encode('utf8')
        content_list = response.xpath('//div[@id="p_content"]/p/text()').extract()
        content = "".join(content_list).strip().encode('utf8')
        
        #Store the file by year/month
        year = time[0:4].encode('utf8')
        month = time[5:7].encode('utf8')
        path = base_dir + '/' + year + '/' + month
        #If the dir does not exists, make it
        if not os.path.exists(path):
            os.makedirs(path)
        #If the time_list or the content_list is empty,Means we get the wrong page
        #Do not create the file
        if time_list and content_list:
            filename = path + '/' + title + '.txt'
            with open(filename, "wb") as f:
                f.write(content)
