# coding:utf-8
import scrapy
import random
import requests
import re
from scrapy.selector import Selector
from scrapy.http.cookies import CookieJar



class QuotesSpider(scrapy.Spider):
    name = "dianping"
    
    def __init__(self):
        super(QuotesSpider, self).__init__()
        self.stand_urls = set()
        self.cookie = {"Cookie":"_lxsdk_cuid=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _lxsdk=1612165dafac8-044cab56dee3a4-32637402-13c680-1612165dafbc8; _hc.v=6434107d-a90d-54b4-c801-9b0ae451b322.1516683779; s_ViewType=10; __utma=1.379189273.1520856175.1520856175.1520856175.1; __utmz=1.1520856175.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aburl=1; __utma=1.562503323.1520923756.1520923756.1520923756.1; __utmz=1.1520923756.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cy=2; cye=beijing; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=1623c920cf4-1a9-31f-42b%7C%7C10"}

   
    def start_requests(self):
        urls = [
            'http://www.dianping.com/shopall/2/0',
            # 'http://www.dianping.com/shop/96062595/review_all'
        ]
        for url in urls:
            yield scrapy.Request(url=url)

    def parse(self, response):
        hxs = Selector(response)
        urls = hxs.css('dl')[1].css('li').css('a').xpath('@href').extract()
        yield scrapy.Request(url = 'http:' + urls[0], callback = self.parse_basic_url, cookies=self.cookie) 
        # for url in urls:
        #     yield scrapy.Request(url = 'http:' + url, callback = self.parse_basic_url) 
            
        
    def parse_basic_url(self, response):
        hxs = Selector(response)
        urls = hxs.css('ul').css('li').css('a').xpath('@href').extract()
        with open('stand_url_second.html', 'wb') as f:
            f.write(response.body)
        for url in urls:
            if 'shop' in url and url.split('/')[-1].isdigit():
                self.stand_urls.add(url)
        yield scrapy.Request(url = list(self.stand_urls)[0] + "/review_all/p1", callback= self.parse_stand_url, cookies = self.cookie)
        # for url in self.stand_urls:
        #     yield scrapy.Request(url = url + "/review_all/p1", callback= self.parse_stand_url)
        #     model += 1
        
    def parse_stand_url(self, response):
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
            url = response.url
            print ("title is %s commenter_name is %s and comment_level is %s and comment_stats is %s and comment_descript is %s and url_is %s and comment_detail is %s" %(title, commenter_name, 
            commenter_level, comment_stars, des_list, response.url, comment_detail) )           
        pages = response.xpath('//div[@class="bottom-area clearfix"]/div[@class="reviews-pages"]').css("a::text").extract()
        # 找到 max pages
        max_page_id = max(int(i) for i in pages if i.isdigit())
        basic_page_id = response.url.split("/")[-1][-1]
        print (basic_page_id)
        if int(basic_page_id) <= max_page_id:
            next_url = response.url.rsplit("/", 1)[0] + "/p%s" % (int(basic_page_id) + 1)
            yield scrapy.Request(url = next_url, callback=self.parse_stand_url, cookies = self.cookie)
        
        

    
        
        
        


