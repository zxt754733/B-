# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 18:04:15 2018

@author: 张协涛
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymysql
import re
import time

browser = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

def database(shop, location, title, price, deal, image_url):
    shop = str(shop)
    location = str(location)
    title = str(title)
    price = str(price)
    deal = str(deal)
    image_url = str(image_url)
    try:
        con = pymysql.connect(host='localhost', user='zxt', password='754733.t', db='taobao', charset='utf8')
        cur = con.cursor()
        '''sql_update = "UPDATE food SET shop = %s, location = %s, title = %s, price = %s, deal = %s WHERE image_url = %s"
        cur.execute(sql_update, (shop, location, title, price, deal, image_url))'''
        sql_insert = "insert INTO food (shop, location, title, price, deal, image_url) VALUES (%s, %s, %s, %s, %s, %s);"
        cur.execute(sql_insert, (shop, location, title, price, deal, image_url))
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def search():
    try:
        browser.get('https://www.taobao.com')
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))  # 用selector选择定位输入框
        )
        search_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))  # 定位搜索按钮
        )
        input_box.send_keys('美食')
        search_button.click()
        total_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_products()
        return total_page.text
    except TimeoutError:
        return search()

def next_page(page_number):
    try:
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > "
                                                             "input"))  # 用selector选择定位页码输入框
        )
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > "
                                                         "span.btn.J_Submit"))  # 定位页面搜索按钮
        )
        input_box.clear()
        input_box.send_keys(page_number)
        search_button.click()
        time.sleep(0.5)
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > "
                                                               "li.item.active > span"), str(page_number))
        )
        get_products()
    except TimeoutError:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
            'title': item.find('.title').text(),
            'price': item.find('.price').text()[2:],
            'deal': item.find('.deal-cnt').text()[:-3],
            'image': item.find('.pic .img').attr('data-src')
        }
        database(product['shop'], product['location'], product['title'], product['price'],
                 product['deal'], product['image'])
        print(product)
        time.sleep(0.25)

def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, total + 1):
        next_page(i)
    search()
    browser.close()

if __name__ == '__main__':
    main()
