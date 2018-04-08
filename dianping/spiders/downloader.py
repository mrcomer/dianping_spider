# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http.cookies import CookieJar
import requests


# def test():
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # option = webdriver.ChromeOptions()
    # option.add_argument("disable-infobars")
    # driver = webdriver.Chrome()
    # driver.get("http://www.dianping.com/shop/96062595/review_all/p2")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "p")))
    


    # cap = DesiredCapabilities.PHANTOMJS
    # cap["phantomjs.page.settings.resourceTimeout"] = 1000
    # cap["phantomjs.page.settings.loadImages"] = False
    # cap["phantomjs.page.settings.disk-cache"] = True
    # driver = webdriver.PhantomJS(desired_capabilities=cap)
    # data = driver.get("http://www.dianping.com/shop/96062595")
    # webdriver.support.ui.WebDriverWait(driver, 2)
    # print data.page_source.encode("utf-8")

    # browser = webdriver.Chrome()

    # data = browser.get("http://www.dianping.com/shop/96062595")
    # # data=browser.page_source.encode("utf-8")
    # elem = browser.find_element_by_name("q")
    # print elem
    # with open("/Users/viver/detail.html", 'wb') as f:
    #     f.write(data)

def test_cookies():
    res = requests.get("http://www.dianping.com/beijing/ch10/g110", params={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'})
    print (res.status_code)
    print (res.content)
    

    
if __name__ == "__main__":
    test_cookies()