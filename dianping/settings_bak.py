# -*- coding: utf-8 -*-
# 备用的配置文件
BOT_NAME = 'dianping'

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'

# 禁止机器人协议
ROBOTSTXT_OBEY = False

# 用户代理
USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
]

# IP代理
LOCAL_PROXIES = ['106.46.207.24:33526', '27.154.183.104:29343']

# 禁用COOKies
COOKIES_ENABLED= False

# 下载延迟
DOWNLOAD_DELAY=3

# 中间件配置
DOWNLOADER_MIDDLEWARES = {
#    'dainping.middlewares.MyCustomDownloaderMiddleware': 543,
   'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
   'dianping.middlewares.ProxyMiddleware': 100,

    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':400,
    'dianping.middlewares.RandomUserAgent':100,
}

# mysql 配置
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'databasename'
MYSQL_USER = "username"
MYSQL_PORT = 3306
MYSQL_PASSWD = "passworld"

# 写入数据库
ITEM_PIPELINES = {
    'dianping.pipelines.DianpingPipeline': 300,
}

# redis地址
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_USER = "username"
PASSWORD = "passworld"


# 分布式配置
# 指定使用scrapy-redis的Scheduler
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = True

# 确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 指定排序爬取地址时使用的队列，默认是按照优先级排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 可选的先进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的后进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# 日志级别
LOG_LEVEL = "DEBUG"