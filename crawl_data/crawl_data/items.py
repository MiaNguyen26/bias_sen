# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # h_url = scrapy.Field()
    h_name = scrapy.Field()
    h_reviewer_name = scrapy.Field()
    h_rating = scrapy.Field()
    h_date = scrapy.Field()
    h_title_comment = scrapy.Field()
    h_comment = scrapy.Field()

    # pass
