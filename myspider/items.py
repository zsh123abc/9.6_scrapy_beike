# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    next_url = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    tag = scrapy.Field()
    tag_2 = scrapy.Field()
    location = scrapy.Field()
    acreage = scrapy.Field()
    house_money = scrapy.Field()
    
    alias = scrapy.Field()
    details = scrapy.Field()
    house_album = scrapy.Field()
    pre_sale_permit = scrapy.Field()
    pass
