#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun

import logging
import os
import sys
import time

import schedule
from flask import json

sys.path.append("./")
sys.path.append("../")

from dao import MongoDao
from downloader import download
from html_parser import parse_catalog, parse_chapter, parse_novel_page


def novel_iterator(dao):
    """
    小说迭代器，返回小说实例

    :param dao:
    :return:
    """
    page = 0
    while True:
        results = dao.query_target_novel(page=page)
        if not results: return
        yield from results
        page += 1
    return


def chapter_urls(catalog_url, flag_url):
    """
    返回更新章节列表

    :param catalog_url:
    :param flag_url:
    :return:
    """
    html = download(catalog_url)
    if html:
        return parse_catalog(html, catalog_url, flag_url)
    return []


def update_chapter(chapter_url, novel_id):
    """
    更新章节信息

    :param chapter_url:
    :param novel_id:
    :return:
    """
    try:
        html = download(chapter_url)
        if html:
            # ($title, $content, $url, $number)
            results = parse_chapter(html, chapter_url)
            if results:
                with MongoDao() as dao:
                    dao.insert_novel_chapter(novel_id, results[0], results[1], results[3], results[2])
    except Exception:
        logging.error("更新章节[{}]出错！".format(chapter_url), exc_info=True)


def start():
    """
    启动爬虫

    :return:
    """
    logging.info("启动爬虫，更新小说 ...")

    # 从数据库中检索所有小说
    with MongoDao() as dao:
        # 从数据库中查询所有小说列表
        novels = novel_iterator(dao)
        if not novels: return

    # 遍历小说，依次更新之
    for novel in novels:
        logging.debug("正在爬取更新 《%s》 ", novel["novel_name"])
        # 遍历小说列表，依次检查其是否有更新
        # {'number': '20380548', 'original_url': 'https://www.biquge5200.cc/52_52542/20380548.html'}
        novel_id = str(novel["_id"])
        # 获取最新章节，以源url作为更新标志位
        with MongoDao() as dao:
            chapter = dao.query_novel_chapter_latest(novel_id)

        # 如有更新，则将更新部分爬取下来，入库
        new_urls = chapter_urls(novel["novel_catalog_url"], chapter and chapter["original_url"])
        if new_urls:
            for new_url in new_urls:
                update_chapter(new_url, novel_id)

    logging.info("停止爬虫，更新结束 ...")


def check():
    # 这里的地址是使用的docker的主机名，暂时这样用 ~
    check_url = "http://novel_web/new_novels"
    # check_url = "http://localhost/new_novels"
    try:
        content = download(check_url)
        if content:
            urls = json.loads(content)
            if urls:
                for url in urls:
                    # 下载新提交小说主页，需要将之更新到数据库中
                    content = download(url)
                    if content:
                        # 解析网页，抽取
                        novel_info = parse_novel_page(content, url)
                        # 保存小说信息
                        with MongoDao() as dao:
                            dao.upsert_target_novel(novel_info["novel_name"],
                                                    novel_info["novel_author"],
                                                    novel_info["novel_cover"],
                                                    novel_info["novel_catalog_url"])
            # 主动启动爬虫更新数据
            start()
    except BaseException:
        pass


if __name__ == '__main__':

    # 每天19:00更新小说
    schedule.every().day.at(os.getenv("SCHEDULE_AT", "19:00")).do(start)

    # 增加一个固定任务（每30秒检查一次），检查固定URL，该URL返回一组小说URL列表，表示新增小说，将启动爬虫主动更新
    schedule.every(30).seconds.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)
