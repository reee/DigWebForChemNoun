from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import os
import uuid
from boilerpipe.extract import Extractor

# Define the site we are going to crawl
site_name = "guokr"

# Define where we put the files
base_dir = '/data/site_data/'
data_dir = base_dir + site_name

class GuokrSpider(CrawlSpider):
    name = "guokr"
    allowed_domains = ["www.guokr.com"]
    start_urls = [
            "http://www.guokr.com/scientific/all/archive/201702/"
    ]

    rules = (
        Rule(LinkExtractor(allow=('/article/\d+/?$')), callback='parse_data'),
        Rule(LinkExtractor(allow=('/all/archive/201[0-6][0-1][0-9]/(\?page=\d+)?$')), follow=True),
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
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        content = extractor.getText().encode('utf-8')

        filename = path + '/' +  str(uuid.uuid4()) + '.txt'
        with open(filename, 'wb') as f:
                f.write(content)
