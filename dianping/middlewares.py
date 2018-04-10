import random
import base64
from dianping.settings import LOCAL_PROXIES, USER_AGENTS
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy import log
from dianping.utils import RedisCli, load_proxies


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
    def __init__(self):
        self.redis_cli = RedisCli.get_redis_cli()
        
    def process_request(self, request, spider):
        if len(LOCAL_PROXIES) == 0:
            ip_count = self.redis_cli.scard("proxies")
            if ip_count:
                if ip_count < 5:
                    load_proxies()
            else:
                load_proxies()

            for _ in range(5):
                ip = self.redis_cli.spop("proxies")
                if not ip:
                    continue
                LOCAL_PROXIES.append(str(ip, encoding = "utf8"))
            
        proxy = random.choice(LOCAL_PROXIES)
        print (LOCAL_PROXIES)
        print ("currant_ip_proxy_is_%s ********" %proxy)
        request.meta['proxy'] = "http://%s" % proxy
        return None