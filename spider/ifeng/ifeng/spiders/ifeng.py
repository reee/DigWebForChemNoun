from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os
import uuid
import re
from boilerpipe.extract import Extractor

# Define the site we are going to crawl
site_name = "ifeng"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

class GuokrSpider(CrawlSpider):
    name = "ifeng"
    allowed_domains = ["news.ifeng.com"]
    start_urls = [
            "http://news.ifeng.com/listpage/11502/20110101/1/rtlist.shtml"
    ]

    rules = (
        Rule(LinkExtractor(allow=('.+/detail_201[0-6]_\d{2}/\d{2}/\d+_\d.shtml')), callback='parse_data_old'),
        Rule(LinkExtractor(allow=('/a/201[0-6]\d{4}/\d+_\d.shtml')), callback='parse_data_new'),
        Rule(LinkExtractor(allow=('/listpage/11502/201[0-6]\d{4}/\d+/rtlist.shtml$')), follow=True)
    )

    def parse_data_old(self, response):
        # get the publish time and store the fils by year/month
        time = re.findall("/detail_201[0-6]_\d{2}/\d{2}/", response.url)[0]
        year = time[8:12]
        month = time[13:15]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        # We use boilerpipe to auto extact body from html
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        content = extractor.getText().encode('utf-8')
        #content_list = response.xpath('//*[@id="artical_real"]//text()').extract()
        #content = "".join(content_list).strip().encode("utf8")

        #filename = path + '/' +  title + '.txt'
        filename = path + '/' + str(uuid.uuid4()) + '.txt'
        with open(filename, 'wb') as f:
                f.write(content)

    def parse_data_new(self, response):
         # get the publish time and store the fils by year/month
         time = re.findall("/a/20\d{6}/", response.url)[0][3:11]
         year = time[0:4]
         month = time[4:6]
         path = data_dir + '/' + year + '/' + month
         if not os.path.exists(path):
             os.makedirs(path)
         # get the title
         extractor = Extractor(extractor='ArticleExtractor', html=response.body)
         content = extractor.getText().encode('utf-8')

         #filename = path + '/' +  title + '.txt'
         filename = path + '/' + str(uuid.uuid4()) + '.txt'
         with open(filename, 'wb') as f:
                 f.write(content)
