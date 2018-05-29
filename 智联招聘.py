# -*- coding: utf-8 -*-
'''
Created on 2018/5/5 22:20
Author  : zxt
File    : 智联招聘.py
Software: PyCharm
'''


from pyquery import PyQuery as pq
import requests
import pymysql
import time
import six
import re

def get_city_companies(html):
    res = requests.get(html)
    res.encoding = 'gb2312'
    data = res.text
    # print(data)
    city_companies = re.findall(r'<a.*?href="(.*?)".*?_blank">(.*?)</a>', data)
    # print(city_companies)
    for city_company in city_companies[:33]:
        print(city_company[1] + ':  https:' + city_company[0])
        city_companie_url = 'https:' + city_company[0]
        partition_pages(city_companie_url)

def partition_pages(html):
    html = html + 'p1'
    for page in range(1, 100):
        print('page:' + str(page))
        html = re.sub(r'(\d+)', str(page), html)
        print(html)
        get_company_url(html)
        time.sleep(2)

def get_company_url(html):
    res = requests.get(html)
    res.encoding = 'utf-8'
    data = res.text
    # print(data)
    companies_url = re.findall(r'href="(http://company\.zhaopin\.com/CC\d+\.htm)".*?</a>', data)
    for company_url in companies_url:
        print(company_url)
        company_info(company_url)

def company_info(html):
    data = pq(html)
    # print(data)
    positions = data('.cLeft').items()
    briefs = data('.mainLeft').items()
    for brief, position in six.moves.zip(briefs, positions):
        company_brief = brief.find('.comTinyDes span').text().split()
        # print(company_brief)
        details = data('.company-content').text().split()
        # print(details)
        job_infos = position.find('span').text().split()
        job_info = job_infos[3:]
        job_duty = position.find('p').text().split()
        company = {
            'name': brief.find('h1').text(),
            'address': brief.find('.comAddress').text(),
            'nature': company_brief[1],
            'size': company_brief[3],
            'industry': company_brief[-3],
            'details': details[1] + details[2],
            'job_requirements': job_info[0] + '; ' + job_info[1],
            'job_duty': ''.join(job_duty)
        }
        print(company)

def main():
    html = 'https://www.zhaopin.com/jobseeker/index_industry.html'
    get_city_companies(html)

if __name__ == '__main__':
    main()