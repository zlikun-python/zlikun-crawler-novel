#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import logging

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
        pass
    pass


if __name__ == '__main__':
    logging.debug("--begin--")
    start()
    logging.debug("--end--")
