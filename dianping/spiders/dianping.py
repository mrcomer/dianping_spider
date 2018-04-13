# coding:utf-8
import scrapy
import random
import requests
import re
import logging
from scrapy.selector import Selector
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
from dianping.items import DianpingItem
from dianping.settings import LOCAL_PROXIES, HTTPERROR_ALLOWED_CODES
from dianping.utils import RedisCli


class BaseUrlSpider(scrapy.Spider):
    name = "base_url"

    def __init__(self):
        super(BaseUrlSpider, self).__init__()
        


class QuotesSpider(scrapy.Spider):
    name = "dianping"
    
    def __init__(self):
        super(QuotesSpider, self).__init__()
        self.redis_cli = RedisCli().get_redis_cli()

        # self.city_dict = {1:"shanghai", 2:"beijing", 3:"hangzhong", 4:"guangzhou", 5:"nanjing", 6:"suzhou", 7:"shenzheng", 8:"chengdu",
        # 9:"chongqing", 10:"tianjing", 11:"ningbo", 12:"yangzhou", 13:"wuxi", 14:"guzhou", 15:"xiamen", 16:"wuhan", 17:"xian", 18:"shenyang", 19:"dalian"
        # }
        self.city_dict = {1:"shanghai", 3:"hangzhong", 4:"guangzhou", 5:"nanjing", 6:"suzhou", 7:"shenzheng", 8:"chengdu",
        9:"chongqing", 10:"tianjing",12:"yangzhou", 13:"wuxi", 14:"guzhou", 15:"xiamen", 16:"wuhan", 17:"xian", 18:"shenyang", 19:"dalian"
        }
        self.cookie = {"Cookie":"_lxsdk_cuid=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _lxsdk=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _hc.v=6434107d-a90d-54b4-c801-9b0ae451b322.1516683779; s_ViewType=10; __utma=1.379189273.1520856175.1520856175.1520856175.1; __utmz=1.1520856175.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aburl=1; __utma=1.562503323.1520923756.1520923756.1520923756.1; __utmz=1.1520923756.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cy=2; cye=beijing; _lxsdk_s=162aa4b5285-d6e-08a-a2e%7C%7C252"}

   
    def start_requests(self):
        for key, value in self.city_dict.items():
            url = 'http://www.dianping.com/shopall/%s/0' % key
            yield scrapy.Request(url=url, meta={'city':value})

    
    def del_ip(self, ip):
        LOCAL_PROXIES.remove(ip)
        

    def parse(self, response):
        hxs = Selector(response)
        if int(response.status) in HTTPERROR_ALLOWED_CODES:
            self.del_ip(response.meta['proxy'].split("//")[1])

        urls = hxs.css('dl')[1].css('li').css('a').xpath('@href').extract()
        # yield scrapy.Request(url = 'http:' + urls[0], callback = self.midle_url, cookies=self.cookie) 
        for url in urls:
            yield scrapy.Request(url = 'http:' + url , callback= self.midle_url, meta={'city':response.meta['city']})
    
    def midle_url(self, response):
        hxs = Selector(response)
        pages = hxs.xpath('//div[@class="page"]').css("a::text").extract()
        try:
            max_page_id = max(int(i) for i in pages if i.isdigit())
        except Exception as e:
            max_page_id = 0 
            logging.info("error_log_reset_max_page_id")

        if not max_page_id:
            yield scrapy.Request(url = response.url, callback = self.parse_basic_url, meta={'city':response.meta['city']}) 
        else:
            for i in range(1, max_page_id+1):
                yield scrapy.Request(url = response.url + "p%s"%i, callback=self.parse_basic_url,meta={'city':response.meta['city']})
      
        

        
    def parse_basic_url(self, response):
        if int(response.status) in HTTPERROR_ALLOWED_CODES:
            self.del_ip(response.meta['proxy'].split("//")[1])
        hxs = Selector(response)
        urls = hxs.css('ul').css('li').css('a').xpath('@href').extract()
        for url in urls:
            if 'shop' in url and url.split('/')[-1].isdigit():
                self.redis_cli.sadd("%s_stand_url"%response.meta['city'], url)
        

    
class DetailSpider(scrapy.Spider):
    name="detail_info"
    def __init__(self):
        super(DetailSpider, self).__init__()
        self.redis_cli = RedisCli().get_redis_cli()
        self.city_dict = {1:"shanghai", 2:"beijing", 3:"hangzhong", 4:"guangzhou", 5:"nanjing", 6:"suzhou", 7:"shenzheng", 8:"chengdu",
        9:"chongqing", 10:"tianjing", 11:"ningbo", 12:"yangzhou", 13:"wuxi", 14:"guzhou", 15:"xiamen", 16:"wuhan", 17:"xian", 18:"shenyang", 19:"dalian"
        }
        self.cookie = {"Cookie":"_lxsdk_cuid=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _lxsdk=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _hc.v=6434107d-a90d-54b4-c801-9b0ae451b322.1516683779; s_ViewType=10; __utma=1.379189273.1520856175.1520856175.1520856175.1; __utmz=1.1520856175.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aburl=1; __utma=1.562503323.1520923756.1520923756.1520923756.1; __utmz=1.1520923756.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cy=2; cye=beijing; _lxsdk_s=162aa4b5285-d6e-08a-a2e%7C%7C252"}
    
    def start_requests(self):
        for values in self.city_dict.values():
            count = self.redis_cli.scard("%s_stand_url"% values)
            for _ in range(count):
                url = self.redis_cli.spop("%s_stand_url"% values)
                url = str(url, encoding = "utf8")
                self.redis_cli.sadd("%s_finish_url" % values, url)
                yield scrapy.Request(url = url + "/review_all/p1", callback=self.parse_stand_url, meta={'city':values})

    def del_ip(self, ip):
        try:
            LOCAL_PROXIES.remove(ip)
        except Exception as e:
            logging.info(e.message)
            
    def parse_stand_url(self, response):
        #淘汰失效IP
        if int(response.status) in HTTPERROR_ALLOWED_CODES:
            self.del_ip(response.meta['proxy'].split("//")[1])
        items = DianpingItem()
        hxs = Selector(response)
        # 被评论的商家
        title = hxs.css('h1').css('a').xpath('@title').extract_first()
        # 获取所有的评论信息
        comment_list = hxs.xpath('//div[@class="reviews-items"]/ul/li')
        for item in range(len(comment_list)):
            des_list = []
            commenter_name = comment_list[item].xpath('div[@class="main-review"]/div[@class="dper-info"]').css("a::text").extract_first()
            commenter_level = comment_list[item].xpath('div[@class="main-review"]/div[@class="dper-info"]/span/@class').extract_first()
            if commenter_level:
                commenter_level = "".join(re.findall(r'\d+', commenter_level.split(" ")[1]))
            comment_stars = comment_list[item].xpath('div[@class="main-review"]/div[@class="review-rank"]/span/@class').extract_first()
            if comment_stars:
                comment_stars = "".join(re.findall(r'\d+', comment_stars.split(" ")[1]))

            comment_descript = comment_list[item].xpath('div[@class="main-review"]/div[@class="review-rank"]/span[@class="score"]').css("span::text").extract()
            for i in comment_descript:
                des = re.findall(r'\w+', i)
                if des:
                    des_list.append("".join(des))
            
            comment_detail = comment_list[item].xpath('div[@class="main-review"]/div[@class="review-words Hide"]/text()').extract_first()

            items['title'] = title
            items['commenter_name'] = commenter_name
            items['commenter_level'] = commenter_level
            items['comment_stars'] = comment_stars
            items['comment_descript'] = des_list
            items['shop_url'] = response.url
            items['comment_detail'] = comment_detail
            items['city'] = response.meta.get("city", "other")
            yield items 

                 
        pages = response.xpath('//div[@class="bottom-area clearfix"]/div[@class="reviews-pages"]').css("a::text").extract()
        # 找到 max pages
        try:
            max_page_id = max(int(i) for i in pages if i.isdigit())
        except Exception as e:
            max_page_id = 0 
            logging.info("error_log_reset_max_page_id")

        basic_page_id = response.url.split("/")[-1][1:]
        if int(basic_page_id) <= max_page_id:
            next_url = response.url.rsplit("/", 1)[0] + "/p%s" % (int(basic_page_id) + 1)
            yield scrapy.Request(url = next_url, callback=self.parse_stand_url, cookies=self.cookie)
        
        
        