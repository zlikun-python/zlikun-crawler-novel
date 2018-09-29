#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import asyncio

import aiohttp
from downloader import download
from pyquery import PyQuery


async def parse_chapter(html, url):
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


async def parse_catalog(html, url, flag_url=None):
    """
    章节列表解析器

    :param html: 要解析的网页正文
    :param url: 要解析的网页URL
    :param flag_url: 用于过滤已处理过URL的标记URL，按顺序遍历章节列表，取该标记之后（不包含flag_url）的URL
    :return: [(id, url), (id, url), ...]
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
            chapters.append((i - 8, href))

    return chapters


async def parse_novel_page(html, url):
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


async def testing():
    async with aiohttp.ClientSession() as session:
        # 章节列表页
        url = "https://www.biquge5200.cc/52_52542/"
        html = await download(session, url)

        # 测试解析章节列表
        catalog_data = await parse_catalog(html, url)
        print(catalog_data)

        # 测试解析小说信息
        novel_data = await parse_novel_page(html, url)
        print(novel_data)

        # 章节正文页
        url = "https://www.biquge5200.cc/52_52542/20380548.html"
        html = await download(session, url)

        # 测试解析章节正文
        chapter_data = await parse_chapter(html, url)
        print(chapter_data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()

    # 测试过滤器
    # 大漠孤烟直，    长河落日圆。    一望无垠的大漠，...
    print(content_filter("大漠孤烟直，&nbsp;&nbsp;&nbsp;&nbsp;长河落日圆。&nbsp;&nbsp;&nbsp;&nbsp;一望无垠的大漠，..."))
