from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "iupac"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name + '/'

class IUPACSpider(CrawlSpider):
    name = site_name
    allowed_domains = ["goldbook.iupac.org"]
    start_urls = [
        "http://goldbook.iupac.org/index-all.html",
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/[A-Z]\d{5}.html$')), callback='parse_data'),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        en_name = response.xpath('//div[@id="cast-hesla"]/h1//text()').extract()[0].strip().encode('utf-8')
        en_names_file = data_dir + "goldbook_en.txt"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(en_names_file, 'a') as fe:
            fe.write(en_name)
            fe.write("\n")
