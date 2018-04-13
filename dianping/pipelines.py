# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from dianping import settings
from dianping.items import DianpingItem

class DianpingPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            port = settings.MYSQL_PORT,
            charset = 'utf8mb4'
        )
        self.cursor = self.connect.cursor()
        
    def process_item(self, item, spider):
        title = item.get("title");
        commenter_name = item.get("commenter_name")
        commenter_level = item.get("commenter_level")
        comment_stars = item.get("comment_stars")
        comment_descript = item.get("comment_descript")
        shop_url = item.get("shop_url")
        comment_detail = item.get("comment_detail")
        city = item.get("city")

        sql = u"""
            insert into dp_script_stand (shop_name, commenter_name, commenter_level,
            comment_stars, comment_descript,shop_url,comment_detail, city)
            values("%s", "%s", %s, %s, "%s", "%s", "%s", "%s")
        """%(title, commenter_name, commenter_level, comment_stars, comment_descript, shop_url, comment_detail, city)
        self.cursor.execute(sql)
        self.connect.commit()
        return item
       

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
