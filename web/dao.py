#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import datetime
import logging

from bson import json_util, ObjectId
from pymongo import MongoClient, DESCENDING

import config
import utils


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

    def query_novel(self, novel_id):
        """
        查询指定小说

        :param novel_id:
        :return:
        """
        collection = self.db.novel
        return collection.find_one({"_id": ObjectId(novel_id)})

    def query_novel_chapter_catalog(self, novel_id):
        """
        查询小说章节列表，标题、内容、源网页

        :param novel_id:
        :return:
        """

        # 一次读取整本小说的章节列表数据
        cursor = self.db.chapter.find({"novel_id": novel_id}, {"_id": 1, "title": 1})
        # 将_id转换为字符串
        return [(str(data["_id"]), data["title"]) for data in cursor]

    def query_novel_chapter(self, chapter_id):
        """
        查询小说章节正文数据

        :param chapter_id:
        :return:
        """
        collection = self.db.chapter
        oid = ObjectId(chapter_id)
        # 查询该章节的上一章和下一章
        prev_chapter = utils.get_first_from_list(
            [item for item in collection.find({"_id": {"$lt": oid}}, {"title": 1}).limit(1)])
        next_chapter = utils.get_first_from_list(
            [item for item in collection.find({"_id": {"$gt": oid}}, {"title": 1}).limit(1)])

        # 查询章节信息
        return {"curr_chapter": collection.find_one({"_id": oid},
                                                    {"title": 1, "content": 1, "original_url": 1}),
                "prev_chapter": prev_chapter,
                "next_chapter": next_chapter}


if __name__ == '__main__':
    with MongoDao() as dao:

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
        logging.debug(dao.query_novel_chapter_catalog("5ba789bb664952eb0c36f93a"))

        # 查询小说章节正文
        logging.debug(dao.query_novel_chapter("5ba83a8214170f5a5c80d94a"))
