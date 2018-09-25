#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun

import logging
import os
import sys
import time

import schedule

sys.path.append("./")
sys.path.append("../")

from dao import MongoDao
from downloader import download
from html_parser import parse_catalog, parse_chapter


def novel_iterator(dao):
    """
    小说迭代器，返回小说实例

    :param dao:
    :return:
    """
    page = 0
    while True:
        results = dao.list_novel(page=page)
        if not results:
            return
        yield from results
        page += 1
    return


def chapter_urls(novel_origin_url, flag_url):
    """
    返回更新章节列表

    :param novel_origin_url:
    :param flag_url:
    :return:
    """
    html = download(novel_origin_url)
    if html:
        return parse_catalog(html, novel_origin_url, flag_url)
    return []


def update_chapter(chapter_origin_url, novel_id):
    """
    更新章节信息

    :param chapter_origin_url:
    :param novel_id:
    :return:
    """
    try:
        html = download(chapter_origin_url)
        if html:
            # ($title, $content, $url)
            results = parse_chapter(html, chapter_origin_url)
            if results:
                with MongoDao() as dao:
                    dao.save_chapter(novel_id, {"title": results[0], "content": results[1], "origin_url": results[2]})
    except BaseException:
        logging.error("更新章节[{}]出错！".format(chapter_origin_url))


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
        logging.debug("正在爬取更新 《%s》 ", novel["name"])
        # 遍历小说列表，依次检查其是否有更新
        # {'number': '20380548', 'original_url': 'https://www.biquge5200.cc/52_52542/20380548.html'}
        novel_id = str(novel["_id"])
        # 获取最新章节，以源url作为更新标志位
        with MongoDao() as dao:
            chapter = dao.get_latest_chapter(novel_id)

        # 如有更新，则将更新部分爬取下来，入库
        new_urls = chapter_urls(novel["origin_url"], chapter and chapter["origin_url"])
        if new_urls:
            for new_url in new_urls:
                update_chapter(new_url, novel_id)

    logging.info("停止爬虫，更新结束 ...")


if __name__ == '__main__':
    # 每次启动时运行一次爬虫
    start()

    # 每天19:00更新小说
    schedule.every().day.at(os.getenv("SCHEDULE_AT", "19:00")).do(start)

    while True:
        schedule.run_pending()
        time.sleep(1)
