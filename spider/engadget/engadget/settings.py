# -*- coding: utf-8 -*-

# Scrapy settings for engadget project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'engadget'

SPIDER_MODULES = ['engadget.spiders']
NEWSPIDER_MODULE = 'engadget.spiders'

AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 115Browser/5.1.3'
