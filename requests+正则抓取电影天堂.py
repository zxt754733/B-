# -*- coding: utf-8 -*-
'''
Created on 2018/5/23 16:07
Author  : zxt
File    : requests+正则抓取电影天堂.py
Software: PyCharm
'''

from requests.exceptions import RequestException
import requests
import pymysql
import time
import re


def get_partition_url(html):
    try:
        res = requests.get(html)
        res.encoding = 'gbk'
        data = res.text
        partition = re.compile('<li.*?href="(.*?)">(.*?)</a>.*?/li>', re.S)
        results = re.findall(partition, data)
        # print(results)
        for result in results[2:10]:
            if len(result[0]) < 30:
                res = 'http://www.ygdy8.net' + result[0]
            else:
                res = result[0]
            # print(res)
            time.sleep(2.5)
            get_partition_page(res)
    except RequestException as rex:
        print(rex)

def get_movie_url(html):
    res = requests.get(html)
    res.encoding = 'gbk'
    data = res.text
    partition = re.compile('<.*?x".*?href="(.*?)".*?/a>', re.S)
    results = re.findall(partition, data)
    # print(results)
    for result in results[1:26]:
        # print(result[0])
        res = 'http://www.ygdy8.net' + result
        # print(res)
        get_movie_info(res)
        time.sleep(0.25)

def get_partition_page(html):
    res = requests.get(html)
    res.encoding = 'gbk'
    data = res.text
    # print(data)
    # rc = re.compile(r'^value="(.*?)">\d+</option>$', re.S)
    results = re.findall(r"option value='(.*?)'.*?option>", data)
    for result in results:
        res = html.replace("index.html", result)
        print(result)
        get_movie_url(res)
        time.sleep(1.5)

def get_movie_info(html):
    res = requests.get(html)
    res.encoding = 'gbk'
    data = res.text
    movie_title = re.findall(r'<font color=#07519a>(.*?)</font>', data)
    movietitle = movie_title[0]
    # print("电影名称：")
    # print(movie_title[0])
    img_url = re.findall(r'<img.*?0.*?src="(.*?)".*?/>', data)
    # print("电影海报：")
    iu = "  ".join(img_url)
    # print(iu)
    movie_magnet = re.findall(r'<td.*?#fdfddf.*?href.*?">(ftp.*?)</a></td>', data)
    if movie_magnet:
        mm = movie_magnet[0]
    else:
        mm = movie_magnet
    # print("磁力链接：" + movie_magnet[0])
    movie_infos = re.findall(r'<br /><br />(.*?)<br /><br /><img.*?>', data)
    # print("电影信息：")
    movie_info = " ".join(movie_infos).replace('<br />', " ")
    movie_info = re.sub(r'<img.*?>', '', movie_info)
    # print(mi)
    try:
        save_to_mysql(movietitle, iu, mm, movie_info)
        print('数据库已插入成功')
    except Exception as e:
        print('数据库插入失败：' + e)

def save_to_mysql(movie_title, imgurl, movie_magnet, movieinfo):
    movie_title = str(movie_title)
    imgurl = str(imgurl)
    movie_magnet = str(movie_magnet)
    movieinfo = str(movieinfo)
    try:
        con = pymysql.connect(host='localhost', user='zxt', password='754733.t', db='电影天堂', charset='utf8')
        cur = con.cursor()
        sql = "insert ignore into 电影天堂分区电影 (电影名称, 电影海报与截图, 迅雷下载链接, 电影信息) values (%s, %s, %s, %s);"
        cur.execute(sql, (movie_title, imgurl, movie_magnet, movieinfo))
        con.commit()
        con.close()
        cur.close()
    except Exception as e:
        print(e)

def main():
    html = 'http://www.dytt8.net/'
    get_partition_url(html)

if __name__ == '__main__':
    main()
