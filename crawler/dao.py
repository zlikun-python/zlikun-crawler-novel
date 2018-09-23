#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import datetime
import logging

from bson import json_util
from pymongo import MongoClient, DESCENDING

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

    def query_target_novel(self, page=0, limit=5):
        """
        查询小说列表，分页查询

        :param page:
        :param limit:
        :return:
        """
        collection = self.db.novel
        # 查询排除"update_time"字段，由"projection"参数控制，0表示排除
        cursor = collection.find({}, {"update_time": 0}).skip(page * limit).limit(limit)
        return [data for data in cursor]

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

    def query_novel_chapter_latest(self, novel_id):
        """
        查询小说章节列表最后一个章节编号和原始url信息

        :param novel_id:
        :return:
        """

        # 下面这种做法性能较差，数据规模小时临时用一下，后面应把最后一条记录写入缓存或数据库，直接查询比较好
        cursor = self.db.chapter.find({"novel_id": novel_id},
                                      {"_id": 0, "number": 1, "original_url": 1}).sort("_id", DESCENDING).limit(1)
        # 可能没有数据，所以返回迭代器里的下一个元素，当遇到StopIteration时返回None
        try:
            return next(cursor)
        except StopIteration:
            return None

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
            "original_url": original_url,
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

        # 查询小说列表
        """
        {
            "_id": {
                "$oid": "5ba789bb664952eb0c36f93a"
            },
            "novel_author": "\u8fb0\u4e1c",
            "novel_name": "\u5723\u589f",
            "novel_catalog_url": "https://www.biquge5200.cc/52_52542/",
            "novel_cover": "http://r.m.biquge5200.cc/cover/aHR0cDovL3FpZGlhbi5xcGljLmNuL3FkYmltZy8zNDk1NzMvMTAwNDYwODczOC8xODA="
        }
        """
        for novel in dao.query_target_novel():
            logging.debug(json_util.dumps(novel, indent=4))

        # 查询指定小说最新章节
        # {'number': '20380548', 'original_url': 'https://www.biquge5200.cc/52_52542/20380548.html'}
        logging.debug(dao.query_novel_chapter_latest("5ba789bb664952eb0c36f93a"))
