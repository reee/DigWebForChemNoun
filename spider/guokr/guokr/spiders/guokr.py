from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os

# Define the site we are going to crawl
site_name = "guokr"

# Define where we put the files
base_dir = '/Data/site_data/'
data_dir = base_dir + site_name

class GuokrSpider(CrawlSpider):
    name = "guokr"
    allowed_domains = ["www.guokr.com"]
    start_urls = [
        "http://www.guokr.com/scientific/subject/chemistry",
        "http://www.guokr.com/scientific"
    ]

    rules = (
        Rule(LinkExtractor(allow=('/article/\d+/?$')), callback='parse_data', follow=True,),
    )


    def parse_data(self, response):
        # get the publish time and store the fils by year/month
        time_list = response.xpath('//meta[@itemprop="http://purl.org/dc/terms/modified"]/@content').extract()
        time = "".join(time_list).encode("utf8")
        year = time[0:4]
        month = time[5:7]
        path = data_dir + '/' + year + '/' + month
        if not os.path.exists(path):
            os.makedirs(path)
        # get the title
        title_list = response.xpath('//h1[@id="articleTitle"]/text()').extract()
        title = "".join(title_list).strip().encode("utf8")
        # get the content
        content_list = response.xpath('//div[@class="document"]/div//text()').extract()
        content = "".join(content_list).strip().encode("utf8")

        filename = path + '/' +  title + '.txt'
        with open(filename, 'wb') as f:
                f.write(content)
