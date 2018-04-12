# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()


    # 店家名称
    title = scrapy.Field()
    # 评价者昵称
    commenter_name = scrapy.Field()
    # 评价者等级
    commenter_level = scrapy.Field()
    # 点评得分
    comment_stars = scrapy.Field()
    # 主要评价描述
    comment_descript = scrapy.Field()
    # 商家地址
    shop_url = scrapy.Field()
    # 详细的评价
    comment_detail = scrapy.Field()
    # 城市
    city = scrapy.Field()
    