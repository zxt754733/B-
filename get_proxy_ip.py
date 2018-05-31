# -*- coding: utf-8 -*-
'''
Created on 2018/5/30 21:40
Author  : zxt
File    : get_proxy_ip.py
Software: PyCharm
'''

import urllib.request
import threading
import requests
import pymysql
import random
import time
import re


lock = threading.Lock()


def get_proxy(data):
    # print(data)
    ip_port_lists = re.findall(r'<tr.*?odd">(.*?)</tr>', data, re.S)
    proxy_list = []
    for ip_port_list in ip_port_lists:
        ip_list = re.findall(r'(\d+\.\d+\.\d+\.\d+)', ip_port_list, re.S)[0]
        port_list = re.findall(r'<td>(\d+)</td>', ip_port_list, re.S)[0]
        # print(ip_list + '  ' + port_list)
        proxy = '{}:{}'.format(ip_list, port_list)
        # print(proxy)
        proxy_list.append(proxy)
    # print(proxy_list)
    return proxy_list


def proxy_test(proxy_list, i):
    proxy = proxy_list[i]
    print('当前代理ip: {}'.format(proxy))
    sleep_time = random.random()
    print('等待{}秒'.format(sleep_time))
    time.sleep(sleep_time)
    proxy_support = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    req = urllib.request.Request('http://httpbin.org/ip')
    try:
        urllib.request.urlopen(req)
        # print(html)
        lock.acquire()
        print('ip有效')
        ip = re.findall(r'(\d+\.\d+\.\d+\.\d+)', proxy)[0]
        port = re.findall(r':(\d+)', proxy)[0]
        # print(ip + port)
        lock.release()
        database(ip, port)
    except Exception as e:
        lock.acquire()
        print('ip无效')
        print(e)
        lock.release()


def database(ip, port):
    ip = str(ip)
    port = str(port)
    try:
        con = pymysql.connect(host='localhost', user='zxt', password='754733.t', db='proxypool', charset='utf8')
        cur = con.cursor()
        sql = 'insert ignore into proxy_pool (ip, port) values (%s, %s);'
        cur.execute(sql, (ip, port))
        con.commit()
        cur.close()
        con.close()
        print('数据库插入成功')
    except Exception as e:
        print('数据库插入失败')
        print(e)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.139 Safari/537.36'
    }
    for i in range(1, 3000):
        html = 'http://www.xicidaili.com/nn/{}'.format(i)
        # print(html)
        res = requests.get(html, headers=headers)
        res.encoding = 'utf-8'
        data = res.text
        proxy_list = get_proxy(data)
        threads = []
        for j in range(len(proxy_list)):
            proxy_test(proxy_list, j)
            for a in range(len(proxy_list)):
                thread = threading.Thread(target=proxy_test, args=(proxy_list, a))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()


if __name__ == '__main__':
    main()
