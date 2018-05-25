# -*- coding: utf-8 -*-
'''
Created on 2018/4/19 22:58
Author  : zxt
File    : requests+正则爬取猫眼.py
Software: PyCharm
'''

from requests.exceptions import RequestException
import requests
import pymysql
import re

def data_base(name, ranking, image_url, movie_url, dir_or_act, information, score, score_num):
    name = str(name)
    ranking = str(ranking)
    image_url = str(image_url)
    movie_url = str(movie_url)
    dir_or_act = str(dir_or_act)
    information = str(information)
    score = str(score)
    score_num = str(score_num)
    try:
        con = pymysql.connect(host='localhost', user='zxt', password='754733.t', db='豆瓣电影Top250', charset='utf8')
        cur = con.cursor()
        sql = "insert into 豆瓣电影Top250 (片名, 排名, 图片链接, 电影链接, 导演及主演, 影片信息, 评分, 评价人数) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (name, ranking, image_url, movie_url, dir_or_act, information, score, score_num))
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        print(e)

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            parser_one_page(response.text)
        return None
    except RequestException:
        return None

def parser_one_page(html):
    pattern = re.compile('<li.*?class.*?>(\d+)</em>.*?img.*?src="(.*?)".*?hd.*?href="(.*?)".*?title">(.*?)</span>'
                         '.*?bd.*?class.*?>(.*?)<br>(.*?)</p>.*?average">(.*?)</span>.*?content.*?span>.*?span>(.*?)'
                         '</span>', re.S)
    results = re.findall(pattern, html)
    for result in results:
        movie = {
            '片名': result[3],
            '排名': result[0],
            '图片链接': result[1],
            '电影链接': result[2],
            '导演及主演': result[4].strip().replace('&nbsp;', ""),
            '影片信息': result[5].strip().replace('&nbsp;', ""),
            '评分': result[6],
            '评价人数': result[7].strip("人评价")
        }
        data_base(movie['片名'], movie['排名'], movie['图片链接'], movie['电影链接'], movie['导演及主演'],
                  movie['影片信息'], movie['评分'], movie['评价人数'])
        print(movie)

def main():
    for i in range(10):
        m = i * 25
        url = 'https://movie.douban.com/top250?start=%s&filter=' % m
        get_one_page(url)

if __name__ == '__main__':
        main()

