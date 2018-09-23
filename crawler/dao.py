#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import datetime
import logging
import time

from pymongo import MongoClient

import config


class MongoDao:

    def __init__(self, host=config.MONGO_HOST, port=config.MONGO_PORT):
        self.host = host
        self.port = port
        self.db_name = "novels"

    def __enter__(self):
        self.client = MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            logging.error("exc_type = %s, exc_val = %s, exc_tb = %s", exc_type, exc_val, exc_tb)
        self.client.close()

    def upsert_target_novel(self, novel_name, novel_author, novel_cover, novel_catalog_url):
        """
        保存爬虫目标小说信息

        :param novel_name: 小说名
        :param novel_author: 小说作者
        :param novel_cover: 小说封面
        :param novel_catalog_url: 小说目录页URL
        :return:
        """

        data = {
            "novel_name": novel_name,
            "novel_author": novel_author,
            "novel_cover": novel_cover,
            "novel_catalog_url": novel_catalog_url,
            "update_time": datetime.datetime.utcnow(),
        }
        # 小说集合
        collection = self.db.novel
        # 以小说名和作者名为检查条件，重复则更新，不重复则插入
        return collection.update_one({"novel_name": novel_name, "novel_author": novel_author},
                                     {"$set": data},
                                     upsert=True).raw_result

    def insert_novel_chapter(self, novel_id, title, content, number, original_url):
        """
        保存小说章节信息

        :param novel_id: 小说ID（novel集合中的_id值）
        :param title: 章节标题
        :param content: 章节正文
        :param number: 章节编号（目标网站上的编号），两个用途：1. 用于章节排序、2. 用于比较最后爬取的章节，避免重复爬取
        :param original_url: 源章节网页URL
        :return: 插入后的主键（_id）
        """

        data = {
            "novel_id": novel_id,
            "title": title,
            "content": content,
            "number": number,
            "original_chapter_url": original_url,
            "create_time": datetime.datetime.utcnow(),
        }
        collection = self.db.chapter
        return collection.insert_one(data).inserted_id


if __name__ == '__main__':
    with MongoDao() as dao:
        # 保存小说信息
        raw_result = dao.upsert_target_novel("圣墟", "辰东",
                                             "http://r.m.biquge5200.cc/cover/aHR0cDovL3FpZGlhbi5xcGljLmNuL3FkYmltZy8zNDk1NzMvMTAwNDYwODczOC8xODA=",
                                             "https://www.biquge5200.cc/52_52542/")
        # {'n': 1, 'nModified': 0, 'upserted': ObjectId('5ba789bb664952eb0c36f93a'), 'ok': 1.0, 'updatedExisting': False}
        # {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
        logging.debug(raw_result)

        # 保存章节信息
        inserted_id = dao.insert_novel_chapter("5ba789bb664952eb0c36f93a",
                                               "第一章 沙漠中的彼岸花",
                                               "大漠孤烟直，长河落日圆。...",
                                               "20380548",
                                               "https://www.biquge5200.cc/52_52542/20380548.html")
        # 5ba78bf414170f59d84b78ed
        logging.debug(inserted_id)
