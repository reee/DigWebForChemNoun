from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "basechem"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name + '/'

class baseChemSpider(CrawlSpider):
    name = site_name
    allowed_domains = ["www.basechem.org"]
    start_urls = [
        "http://www.basechem.org",
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('/chemical/\d+$')), callback='parse_data', follow=True,),
        Rule(LinkExtractor(allow=('/chemical/nav/.\??p?\=?4?$')), follow=True,),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        cn_name = response.xpath('//ul[@class="summary-text"]/li[2]/span/text()').extract()[0].strip().encode('utf-8')
        cn_names_file = data_dir + "basechem_cn.txt"
        en_name = response.xpath('//ul[@class="summary-text"]/li[3]/span/text()').extract()[0].strip().encode('utf-8')
        en_names_file = data_dir + "basechem_en.txt"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(cn_names_file, 'a') as fc:
            fc.write(cn_name)
            fc.write("\n")
        with open(en_names_file, 'a') as fe:
            fe.write(en_name)
            fe.write("\n")
