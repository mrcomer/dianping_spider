# coding:utf-8

import requests
import json
import logging
import sys
import requests
from redis import StrictRedis, ConnectionPool
# from dianping.settings import LOCAL_PROXIES, REDIS_URL



def load_proxies():
    redis_cli = RedisCli.get_redis_cli()
    url = u"""http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=798e6f1278d742dbb5c4663d24a761f4&count=5&expiryDate=0&format=1"""
    response = requests.get(url)
    proxies =  response.json()
    if int(proxies['code']) == 0:
        for item in proxies['msg']:
            
            ip = item['ip'] + ":" + item['port']
            try:
                r = requests.get("http://www.dianping.com/shopall/2/0", proxies={"https":ip}, timeout = 2)
                redis_cli.sadd("proxies", ip)
            except Exception as e:
                print (e.message, ip)
    else:
        for _ in range(3):
            load_proxies()
        return 0


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst

class RedisCli(Singleton):
    @classmethod
    def get_redis_cli(cls):
        pool = ConnectionPool.from_url("redis://:2070lxx%@119.29.67.169:6379/0")
        redis = StrictRedis(connection_pool=pool)
        return redis

if __name__ == '__main__':
    load_proxies()


