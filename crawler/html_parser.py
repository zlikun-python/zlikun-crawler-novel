#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import re

from downloader import download
from pyquery import PyQuery


def parse_chapter(html, url):
    """
    章节正文解析器

    :param html:
    :param url:
    :return: ($title, $content, $url)
    """
    if not html or not url: return
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


def parse_catalog(html, url, flag_url=None):
    """
    章节列表解析器

    :param html: 要解析的网页正文
    :param url: 要解析的网页URL
    :param flag_url: 用于过滤已处理过URL的标记URL，按顺序遍历章节列表，取该标记之后（不包含flag_url）的URL
    :return:
    """
    pq = PyQuery(html, url=url)

    # 提取章节列表
    chapters = []
    flag = False
    for i, e in enumerate(pq('#list dd > a').items()):
        # 忽略前九项，是该站的最新章节，与下面的章节列表有重复
        if i < 9:
            continue
        href = e.attr('href').strip()
        if flag_url is not None:
            # 使用flag标记控制新加入的章节列表
            if flag:
                chapters.append(href)
            # 直到与flag_url相等，才开始计（不包含）
            if href == flag_url:
                flag = True
        else:
            chapters.append(href)

    return chapters


def parse_novel_page(html, url):
    """
    解析小说主页（章节列表页，但提取的是小说相关数据）

    :param html: 要解析的网页正文
    :param url: 要解析的网页URL
    :return:
    """
    pq = PyQuery(html, url=url)

    name = pq("#info > h1").text().strip()
    author = pq("#info > p:eq(0)").text().replace("作\xa0\xa0\xa0\xa0者：", "").strip()
    cover = pq("#fmimg > img").attr("src")

    return {
        "name": name,
        "author": author,
        "cover": cover,
        "catalog_url": url
    }


if __name__ == '__main__':
    # 测试从URL中提取编号
    url = "https://www.biquge5200.cc/52_52542/20380548.html"
    number = re.search(r"/(\d+).html$", url).group(1)
    print(number, url)
    # 测试过滤器
    # 大漠孤烟直，    长河落日圆。    一望无垠的大漠，...
    print(content_filter("大漠孤烟直，&nbsp;&nbsp;&nbsp;&nbsp;长河落日圆。&nbsp;&nbsp;&nbsp;&nbsp;一望无垠的大漠，..."))
    # 测试章节正文解析器
    # ('第一章 沙漠中的彼岸花', '大漠孤烟直，长河落日圆。\n一望无垠的大漠，空旷而高远，...', 'https://www.biquge5200.cc/52_52542/20380548.html', '20380548')
    # print(parse_chapter(download(url), url))
    # 测试章节列表解析器
    url = "https://www.biquge5200.cc/52_52542/"
    # 返回所有章节链接
    print(parse_catalog(download(url), url))
    # 指定标记链接，返回标记之后的链接
    # ['https://www.biquge5200.cc/52_52542/158199227.html', 'https://www.biquge5200.cc/52_52542/158213176.html',
    # 'https://www.biquge5200.cc/52_52542/158263103.html', 'https://www.biquge5200.cc/52_52542/158264558.html']
    print(parse_catalog(download(url), url, "https://www.biquge5200.cc/52_52542/158145109.html"))

    # 测试小说主页解析器
    url = "https://www.biquge5200.cc/76_76490/";
    print(parse_novel_page(download(url), url))
