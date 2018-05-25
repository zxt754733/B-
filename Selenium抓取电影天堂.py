# -*- coding: utf-8 -*-
'''
Created on 2018/5/16 22:58
Author  : zxt
File    : Selenium抓取电影天堂.py
Software: PyCharm
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import requests
import pymysql
import re
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)
browser.get('http://www.dytt8.net/')

def click_url(url):
    try:
        browser.get(url)
        time.sleep(2)
        browser.back()
    except Exception as e:
        print(e)

def get_partition_url(data):
    partition = re.compile('<li.*?href="(.*?)">(.*?)</a>.*?/li>', re.S)
    results = re.findall(partition, data)
    for result in results[2:10]:
        if len(result[0]) < 30:
            res = 'http://www.ygdy8.net' + result[0]
        else:
            res = result[0]
        # print(res)
        click_url(res)
        time.sleep(0.2)

def partition_next_page():



def main():
    res = requests.get('http://www.dytt8.net/')
    res.encoding = 'gbk'
    data = res.text
    get_partition_url(data)

if __name__ == '__main__':
    main()
