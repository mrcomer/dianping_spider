import random
import base64
from dianping.settings import LOCAL_PROXIES, USER_AGENTS
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy import log



class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agetn = ''):
        self.user_agent = USER_AGENTS
    
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        if ua:
            print ("***current useragent: %s ***" % ua)
            request.headers.setdefault('User-Agent', ua)
        else:
            print ("not useragent ")

class ProxyMiddleware(object):
    """随机选择代理"""
    def process_request(self, request, spider):
        proxy = random.choice(LOCAL_PROXIES)
        if not proxy:
            proxy = random.choice(LOCAL_PROXIES)
        print ("currant_ip_proxy_is_%s ********" %proxy)
        request.meta['proxy'] = "http://%s" % proxy
        return None