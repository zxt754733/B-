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


def database(city, name, website, address, nature, size, industry, introduce, job_requirements, job_duty):
    city = str(city)
    name = str(name)
    website = str(website)
    address = str(address)
    nature = str(nature)
    size = str(size)
    industry = str(industry)
    introduce = str(introduce)
    job_requirements = str(job_requirements)
    job_duty = str(job_duty)
    try:
        con = pymysql.connect(host='localhost', user='zxt', password='754733.t', db='智联招聘', charset='utf8')
        cur = con.cursor()
        sql = "insert ignore into 职位信息(城市, 公司, 公司网址,公司地址, 公司性质, 公司规模, 公司行业, 公司介绍, 岗位要求, " \
              "岗位职责) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (city, name, website, address, nature, size, industry, introduce, job_requirements, job_duty))
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)


def get_city_companies(html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.139 Safari/537.36'
    }
    res = requests.get(html, headers=headers)
    res.encoding = 'gb2312'
    data = res.text
    # print(data)
    city_companies = re.findall(r'<a.*?href="(.*?)".*?_blank">(.*?)</a>', data)
    # print(city_companies)
    for city_company in city_companies[:33]:
        print(city_company[1] + ':  https:' + city_company[0])
        city_companie_url = 'https:' + city_company[0]
        city = city_company[1]
        partition_pages(city_companie_url, city)


def partition_pages(html, city):
    html = html + 'p1'
    for page in range(1, 100):
        print('page:' + str(page))
        html = re.sub(r'(\d+)', str(page), html)
        print(html)
        get_company_url(html, city)
        time.sleep(1)


def get_company_url(html, city):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.139 Safari/537.36'
    }
    res = requests.get(html, headers=headers)
    res.encoding = 'utf-8'
    data = res.text
    # print(data)
    companies_url = re.findall(r'href="(http://company\.zhaopin\.com/CC\d+\.htm)".*?</a>', data)
    for company_url in companies_url:
        # print(company_url)
        company_info(company_url, city)


def company_info(html, city):
    data = pq(html)
    # print(data)
    positions = data('.cLeft').items()
    briefs = data('.mainLeft').items()
    for brief, position in six.moves.zip(briefs, positions):
        company_brief = brief.find('.comTinyDes span').text().split()
        # print(company_brief)
        details = data('.company-content').text().split()
        introduce = ''.join(details)
        # print(details)
        job_infos = position.find('span').text().split()
        job_info = job_infos[3:]
        job_duty = position.find('p').text().split()
        company = {
            'city': city,
            'name': brief.find('h1').text(),
            'website': html,
            'address': brief.find('.comAddress').text(),
            'nature': company_brief[1],
            'size': company_brief[3],
            'industry': company_brief[-3],
            'introduce': introduce,
            'job_requirements': job_info[0] + '; ' + job_info[1],
            'job_duty': ''.join(job_duty)
        }
        # print(company)
        try:
            database(company['city'], company['name'], company['website'], company['address'], company['nature'],
                     company['size'], company['industry'], company['introduce'], company['job_requirements'],
                     company['job_duty'])
            print('数据库插入成功！')
        except:
            print('数据库插入失败！')
        time.sleep(0.2)


def main():
    html = 'https://www.zhaopin.com/jobseeker/index_industry.html'
    get_city_companies(html)


if __name__ == '__main__':
    main()