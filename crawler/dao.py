#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import datetime
import logging
from collections import UserDict

from bson import ObjectId
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
        return self.db["chapter_{}".format(novel_id)].find_one({"_id": ObjectId(chapter_id)})

    def get_latest_chapter(self, novel_id):
        """
        获取小说最新章节

        :param novel_id:
        :return:
        """
        cursor = self.db["chapter_{}".format(novel_id)].find({}, {"origin_url": 1}).sort("_id", -1).limit(1)
        try:
            return next(cursor)
        except StopIteration:
            return None

    def save_novel(self, novel):
        """
        保存（如果已存在则更新，判断条件为：书名+作者名）小说信息，返回小说ID

        :param novel:
        :return:
        """
        assert novel, "小说字典参数不能为空"
        if "update_time" not in novel:
            novel["update_time"] = datetime.datetime.utcnow()
        collection = self.db.novel
        return collection.update_one({"name": novel["name"], "author": novel["author"]}, {"$set": novel},
                                     upsert=True).raw_result

    def save_chapter(self, novel_id, chapter):
        """
        保存章节信息，返回章节ID

        :param novel_id:
        :param chapter:
        :return:
        """

        assert novel_id, "小说ID参数不能为空"
        assert chapter, "小说章节字典参数不能为空"
        if "create_time" not in chapter:
            chapter["create_time"] = datetime.datetime.utcnow()
        collection = self.db["chapter_{}".format(novel_id)]
        return collection.insert_one(chapter).inserted_id


if __name__ == '__main__':
    with MongoDao() as dao:
        # 测试保存小说
        novel = UserDict(name="圣墟", author="辰东",
                         cover="http://r.m.biquge5200.cc/cover/aHR0cDovL3FpZGlhbi5xcGljLmNuL3FkYmltZy8zNDk1NzMvMTAwNDYwODczOC8xODA=",
                         origin_url="https://www.biquge5200.cc/52_52542/").data
        # {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
        print(dao.save_novel(novel))

        # 测试保存章节
        chapter = UserDict(title="第一章 沙漠中的彼岸花",
                           content="大漠孤烟直，长河落日圆。...",
                           origin_url="https://www.biquge5200.cc/52_52542/20380548.html").data
        # 5baa2c1aa6c85b3b00f9bc3d
        print(dao.save_chapter("5baa2a141056cceef3aff29d", chapter))

        # 测试查询小说列表
        print(dao.list_novel())

        # 测试查询小说
        print(dao.get_novel("5baa2a141056cceef3aff29d"))

        # 测试查询章节
        print(dao.get_chapter("5baa2a141056cceef3aff29d", "5baa2c9aa6c85b069c0c26e3"))

        # 测试查询小说最新章节
        print(dao.get_latest_chapter("5baa2a141056cceef3aff29d"))
