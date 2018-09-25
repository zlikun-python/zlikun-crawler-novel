#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import logging

from bson import ObjectId
from pymongo import MongoClient

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

    def list_novel(self, page=0, limit=10):
        """
        遍历小说列表，返回ID、名字、作者等信息

        :param page:
        :param limit:
        :return:
        """
        collection = self.db.novel
        cursor = collection.find({}, {"update_time": 0}).skip(page * limit).limit(limit)
        return [data for data in cursor]

    def get_novel(self, novel_id):
        """
        查询小说信息，返回小说信息、章节列表

        :param novel_id:
        :return:
        """
        novel = self.db.novel.find_one({"_id": ObjectId(novel_id)})
        if novel:
            chapters = [item for item in self.db["chapter_{}".format(novel_id)].find({}, {"title": 1})]
            print(chapters)

        return {
            "novel": novel,
            "chapters": chapters
        }

    def get_chapter(self, novel_id, chapter_id):
        """
        查询小说章节信息

        :param novel_id:
        :param chapter_id:
        :return:
        """
        oid = ObjectId(chapter_id)
        collection = self.db["chapter_{}".format(novel_id)]
        curr_chapter = collection.find_one({"_id": oid})

        # 查询该章节的上一章和下一章
        prev_chapter = utils.get_first_item(
            [item for item in collection.find({"_id": {"$lt": oid}}, {"title": 1}).limit(1)])
        next_chapter = utils.get_first_item(
            [item for item in collection.find({"_id": {"$gt": oid}}, {"title": 1}).limit(1)])

        # 查询章节信息
        return {"curr_chapter": curr_chapter,
                "prev_chapter": prev_chapter,
                "next_chapter": next_chapter}


if __name__ == '__main__':
    with MongoDao() as dao:
        # 测试查询小说列表
        print(dao.list_novel())

        # 测试查询小说
        print(dao.get_novel("5baa2a141056cceef3aff29d"))

        # 测试查询章节
        print(dao.get_chapter("5baa2a141056cceef3aff29d", "5baa32c1a6c85b36d430ee1c"))
