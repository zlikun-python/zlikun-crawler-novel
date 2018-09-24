#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
# 实现一个WEB服务，用于配置股价预警任务
import sys

sys.path.append("./")
sys.path.append("../")

import json

from dao import MongoDao
from flask import Flask, render_template, Response, abort

app = Flask(__name__, template_folder="./templates")


@app.route('/', methods=["GET"])
def query_novels():
    """
    小说列表

    :return:
    """

    with MongoDao() as dao:
        novels = dao.query_target_novel()

    return render_template('index.html', novels=novels)


@app.route('/novel/<novel_id>', methods=["GET"])
def query_novel(novel_id):
    with MongoDao() as dao:
        # 查询小说信息
        novel = dao.query_novel(novel_id)
        # 查询章节列表
        catalogs = dao.query_novel_chapter_catalog(novel_id)

    return render_template('catalog.html', novel=novel, catalogs=catalogs)


@app.route('/novel/<novel_id>/<chapter_id>', methods=["GET"])
def query_chapter(novel_id, chapter_id):
    with MongoDao() as dao:
        # 查询章节正文
        result = dao.query_novel_chapter(chapter_id)
        if not result:
            abort(404)
            return

    chapter = result["curr_chapter"]
    # 由于是网页显示用，所以把换行转换为换行标签
    chapter["content"] = chapter["content"].replace("\n", "<br>")
    return render_template('chapter.html',
                           chapter=chapter,
                           novel_id=novel_id,
                           prev_id=result["prev_chapter"] and str(result["prev_chapter"]["_id"]) or None,
                           next_id=result["next_chapter"] and str(result["next_chapter"]["_id"]) or None)


@app.route("/favicon.ico")
def favicon():
    return ""


@app.errorhandler(404)
def page_not_found(error):
    """
    PageNotFound
    :param error:
    :return:
    """
    resp = Response(json.dumps({"error_code": "404"}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    # app.run(debug=True, port=80)
    app.run(host="0.0.0.0", port=80)
