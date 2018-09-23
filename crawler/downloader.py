#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import logging
import time

import requests

import utils

default_headers = {
    "Host": "www.biquge5200.cc",
    "Referer": "https://www.biquge5200.cc"
}


def download(url, headers={}):
    """
    HTTP下载函数，下载失败后会重试三次（重试间隔1秒）

    :param url:
    :param headers:
    :return:
    """
    headers.update(default_headers)
    for _ in range(4):
        try:
            response = requests.get(url, headers=utils.headers(headers))
            response.raise_for_status()
            if response.status_code == requests.codes.ok:
                return response.text
            else:
                logging.warning("下载 {} 返回状态码：{}".format(url, response.status_code))
        except requests.RequestException:
            logging.error("下载 {} 出错！".format(url), exc_info=True)
        time.sleep(1)


if __name__ == '__main__':
    # 下载章节目录
    text = download("https://www.biquge5200.cc/52_52542/")
    print(text)
    # 下载章节正文
    text = download("https://www.biquge5200.cc/52_52542/20380548.html")
    print(text)
