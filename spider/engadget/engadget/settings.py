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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'engadget (+http://www.yourdomain.com)'
