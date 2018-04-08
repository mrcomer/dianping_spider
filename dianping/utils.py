# coding:utf-8

from dianping.settings import LOCAL_PROXIES
import requests
import json
import logging
import sys


def load_proxies():
    url = u"""http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=9bce1dadc38d4b138ada8b0549aaf8ad&count=1&expiryDate=0&format=1"""
    response = requests.get(url)
    proxies =  response.json()
    if int(proxies['code']) == 0:
        return proxies['msg']['ip'] + ":" + proxies['msg']['port']
    else:
        return 0
