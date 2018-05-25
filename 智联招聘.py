# -*- coding: utf-8 -*-
'''
Created on 2018/5/5 22:20
Author  : zxt
File    : 智联招聘.py
Software: PyCharm
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymysql
import time

browser = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])
browser.get('https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&sm=0&p=1')
wait = WebDriverWait(browser, 10)
browser.set_window_size(900, 600)

# def database():


def next_page(page_num):
    try:
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#goto")))
        search_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "body > div.main > div.search_newlist_main > div.newlist_main > form > div.clearfix "
                                  "> div.newlist_wrap.fl > div.pagesDown > ul > li.nextpagego-box > button")
            )
        )
        input_box.clear()
        input_box.send_keys(page_num)
        search_button.click()
        time.sleep(0.5)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "body > div.main > div.search_newlist_main > div.newlist_main > form > div.clearfix "
                                  "> div.newlist_wrap.fl > div.pagesDown > ul > li:nth-child(3) > a"), str(page_num)
            )
        )
        get_job_url()
    except TimeoutError:
        return next_page(page_num)

def get_job_url():
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#newlist_list_content_table > table:nth-child(12) .zwmc")
            )
        )
        html = browser.page_source
        doc = pq(html)
        items = doc("#newlist_list_content_table > table:nth-child(12) .zwmc").items()
        for item in items:
            job_url = item.find(' a').attr('href')
            get_job(job_url)
    except Exception as e:
        print(e)

def get_job(job_url):
    browser.get(job_url)
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body")
            )
        )
        html = browser.page_source
        doc = pq(html)
        company = doc("body > div.top-fixed-box > div.fixed-inner-box")
        for company_info in company:
            com_info = {
                '职位': company_info.find('.f1').text(),
                '公司': company_info.find(' a').text(),
                '公司网址': company_info.find(' h2 a').attr('href')
            }
            print(com_info)
            time.sleep(0.25)
    except Exception as e:
        print(e)

def main():
    for i in range(1, 90):
        next_page(i)
    browser.close()

if __name__ == '__main__':
    main()
