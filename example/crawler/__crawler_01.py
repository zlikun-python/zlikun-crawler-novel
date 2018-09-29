#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
"""
小说爬虫：https://www.biquge5200.cc/
"""
import logging
import time

import requests

from pyquery import PyQuery

logging.basicConfig(level=logging.INFO,
                    datefmt="%Y/%m/%d %H:%M:%S",
                    format="%(asctime)s %(levelname)8s %(process)05d L%(lineno)03d %(funcName)s %(message)s")

default_headers = {
    "Host": "www.biquge5200.cc",
    "Referer": "https://www.biquge5200.cc/"
}

start_url = "https://www.biquge5200.cc/70_70530/"
novel_name = "良陈美锦（沉香灰烬）"
novel_txt_path = "./data/{}.txt".format(novel_name)


def init():
    """
    初始化文件，创建或清空内容

    :return:
    """
    global novel_name
    with open(novel_txt_path, 'w', encoding="utf-8") as f:
        f.write(novel_name)
        f.write("\r\n" * 3)


def download(url):
    for i in range(4):
        try:
            resp = requests.get(catalog_url, headers=default_headers)
            resp.raise_for_status()
            return resp.text
        except (requests.RequestException, BaseException):
            logging.error("下载 %s 出错 !", url)
            time.sleep(i / 10)


def parse_chapters(html, url):
    """
    章节列表解析器

    :param html:
    :param url:
    :return:
    """
    pq = PyQuery(html, url=url)
    # 提取章节列表
    for i, e in enumerate(pq('#list dd > a').items()):
        # 忽略前九项，是该站的最新章节，与下面的章节列表有重复
        if i < 9:
            continue
        href = e.attr('href').strip()
        yield (i - 8, href)


def parse_content(html, url):
    """
    章节正文解析器

    :param html:
    :param url:
    :return: ($title, $content, $url)
    """
    if not html or not url:
        return
    pq = PyQuery(html, url=url)
    title = pq('div.bookname > h1').text().strip()
    content = content_filter(pq('#content').text().strip())
    return title, content, url


def content_filter(content):
    """
    章节正文过滤器

    :param content:
    :return:
    """
    content = content.replace("&nbsp;", " ")
    return content


def append_to_text(number, title, content):
    """
    将内容写入文件

    :param title:
    :param content:
    :return:
    """
    with open(novel_txt_path, 'a', encoding="utf-8") as f:
        f.write("{:04d} - {}".format(number, title))
        f.write("\r\n")
        f.write(content)
        f.write("\r\n" * 2)


if __name__ == '__main__':

    # 1. 初始化
    init()

    # 2. 下载章节列表页
    catalog_url = start_url
    html = download(catalog_url)
    logging.info("download novel: %s", catalog_url)

    # 3. 循环下载章节并提取章节正文
    for (i, url) in parse_chapters(html, catalog_url):
        logging.info("download chapter: %04d - %s", i, url)
        html = download(url)
        if html:
            results = parse_content(html, url)
            if results:
                append_to_text(i, results[0], results[1])
