# -*- coding: utf-8 -*-
'''
Created on 2018/5/5 22:20
Author  : zxt
File    : 智联招聘.py
Software: PyCharm
'''


from pyquery import PyQuery as pq
import threading
import requests
import pymysql
import random
import time
import six
import re


lock = threading.Lock()


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
        city_company_url = 'https:' + city_company[0]
        city = city_company[1]
        partition_pages(city_company_url, city)


def partition_pages(html, city):
    html = html + 'p1'
    for page in range(1, 100):
        print('page:' + str(page))
        html = re.sub(r'(\d+)', str(page), html)
        print(html)
        get_company_url(html, city)
        time.sleep(1)


def get_company_url(html, city):
    headers = {}
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/66.0.3359.139 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/31.0.1623.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/29.0.1547.62 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/29.0.1547.57 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/29.0.1547.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) '
        'Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) '
        'Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) '
        'Chrome/24.0.1295.0 Safari/537.15',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) '
        'Chrome/24.0.1292.0 Safari/537.14',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) '
        'Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) '
        'Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) '
        'Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.6 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/537.11'
    ]
    headers['User-Agent'] = random.choice(user_agent)
    res = requests.get(html, headers=headers)
    status_code = res.status_code
    if status_code == 200:
        res.encoding = 'utf-8'
        data = res.text
        # print(data)
        companies_url = re.findall(r'href="(http://company\.zhaopin\.com/CC\d+\.htm)".*?</a>', data)
        threads = []
        for company_url in companies_url:
            # print(company_url)
            if requests.get(company_url).status_code == 200:
                thread = threading.Thread(target=company_info, args=(company_url, city))
                threads.append(thread)
                thread.start()
            else:
                return
        for thread in threads:
            thread.join()
    else:
        return



def company_info(html, city):
    t1 = time.time()
    data = pq(html)
    # print(data)
    positions = data('.cLeft').items()
    briefs = data('.mainLeft').items()
    for brief, position in six.moves.zip(briefs, positions):
        company_brief = brief.find('.comTinyDes span').text().split()
        # print(company_brief)
        if len(company_brief) < 1:
            return
        elif len(company_brief) < 3:
            return
        else:
            lock.acquire()
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
        lock.release()

        # print(company)
        try:
            database(company['city'], company['name'], company['website'], company['address'], company['nature'],
                     company['size'], company['industry'], company['introduce'], company['job_requirements'],
                     company['job_duty'])
            print(company['name'])
            print('数据库插入成功！')
        except:
            print('数据库插入失败！')
        sleep_time = random.random()
        time.sleep(sleep_time)


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
        con = pymysql.connect(host='localhost', user='root', password='754733.t', db='智联招聘', charset='utf8')
        cur = con.cursor()
        sql = "insert ignore into 职位信息(城市, 公司, 公司网址,公司地址, 公司性质, 公司规模, 公司行业, 公司介绍, 岗位要求, " \
              "岗位职责) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (city, name, website, address, nature, size, industry, introduce, job_requirements, job_duty))
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)


def main():
    html = 'https://www.zhaopin.com/jobseeker/index_industry.html'
    get_city_companies(html)


if __name__ == '__main__':
    main()