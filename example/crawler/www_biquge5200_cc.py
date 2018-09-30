#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
"""
小说爬虫：https://www.biquge5200.cc/
"""
import logging
import os
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

novel_txt_dir = './data'


def init():
    """
    初始化文件存储目录，检查文件存放目录，不存在则生成

    :return:
    """
    if not os.path.exists(novel_txt_dir):
        os.mkdir(novel_txt_dir, mode=0o755)


def novel_txt_path(novel_name):
    """
    生成小说文本文件PATH

    :param novel_name:
    :return:
    """
    global novel_txt_dir
    return "{}/{}.txt".format(novel_txt_dir, novel_name)


class Crawler:

    def __init__(self, novel_name, novel_number):
        """
        使用小说名、章节列表页URL初始化爬虫

        :param novel_name: 小说名称，格式：<小说名称>（<作者名称>）
        :param novel_number: 小说编号（取章节列表页URL最后一部分）
        """
        self.novel_name = novel_name
        if "https" in novel_number:
            self.catalog_url = novel_number
        else:
            self.catalog_url = "https://www.biquge5200.cc/{}/".format(novel_number)

        # 写入小说名称信息
        with open(novel_txt_path(self.novel_name), 'w', encoding="utf-8") as f:
            f.write(novel_name)
            f.write("\r\n" * 2)

    @staticmethod
    def __download(url):
        """
        下载器

        :param url:
        :return:
        """
        global default_headers
        for i in range(4):
            try:
                resp = requests.get(url, headers=default_headers)
                resp.raise_for_status()
                return resp.text
            except (requests.RequestException, BaseException):
                time.sleep(i / 4)

        logging.error("下载 %s 出错 !", url)

    @staticmethod
    def __parse_chapters(html):
        """
        章节列表解析器

        :param html:
        :return:
        """
        pq = PyQuery(html)
        # 提取章节列表
        for i, e in enumerate(pq('#list dd > a').items()):
            # 忽略前九项，是该站的最新章节，与下面的章节列表有重复
            if i < 9:
                continue
            href = e.attr('href').strip()
            yield (i - 8, href)

    def __parse_content(self, html):
        """
        章节正文解析器

        :param html:
        :return: ($title, $content)
        """
        if not html:
            return
        pq = PyQuery(html)
        title = pq('div.bookname > h1').text().strip()
        content = self.__content_filter(pq('#content').text().strip())
        return title, content

    @staticmethod
    def __content_filter(content):
        """
        章节正文过滤器

        :param content:
        :return:
        """
        content = content.replace("&nbsp;", " ")
        return content

    def __append_to_text(self, number, title, content):
        """
        将内容写入文件

        :param title:
        :param content:
        :return:
        """
        with open(novel_txt_path(self.novel_name), 'a', encoding="utf-8") as f:
            f.write("{:04d} - {}".format(number, title))
            f.write("\r\n")
            f.write(content)
            f.write("\r\n" * 2)

    def crawl(self):
        """
        启动爬虫方法

        :return:
        """
        logging.info("小说[%s]开始下载！", self.novel_name)

        # 下载章节列表页
        html = self.__download(self.catalog_url)
        if not html:
            logging.info("小说[%s]下载失败！", self.novel_name)
            return

        # 循环下载章节并提取章节正文
        for (i, url) in self.__parse_chapters(html):
            logging.info("download chapter: %04d - %s", i, url)
            html = self.__download(url)
            if html:
                results = self.__parse_content(html)
                if results:
                    self.__append_to_text(i, results[0], results[1])

        logging.info("小说[%s]下载完成！", self.novel_name)


if __name__ == '__main__':
    # 初始化爬虫
    init()

    # 运行爬虫，允许使用章节列表页全路径和小说编号两种方式来启动爬虫
    # Crawler("剑来（烽火戏诸侯）", "75_75584").crawl()
    # Crawler("剑来（烽火戏诸侯）", " https://www.biquge5200.cc/75_75584/").crawl()
    # Crawler("牧神记（宅猪）", "76_76490").crawl()

    # 读取 ./data/novels.txt 文件来批量下载，格式为：<小说名>,<作者名>,<小说编号>
    with open(r'./data/novels.txt', 'r', encoding='utf-8') as txt:
        for line in txt.readlines():
            if "#" in line:
                continue
            try:
                (name, author, code) = line.split(",")
                Crawler("{}（{}）".format(name.strip(), author.strip()), code.strip()).crawl()
            except:
                logging.error("解析并下载[%s]出错!", line)
