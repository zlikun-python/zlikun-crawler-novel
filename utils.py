#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import json


def headers(ext_headers={}):
    """
    请求消息头

    :param ext_headers:
    :return:
    """
    data = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.132 Safari/537.36",
        "Connection": "keep-alive",
    }
    data.update(ext_headers)
    return data


def get_first_from_list(lst):
    """
    从列表中取得第一个元素，如果列表空，返回None

    :param lst:
    :return:
    """
    if lst:
        return lst[0]
    else:
        return None


if __name__ == '__main__':
    print(json.dumps(headers({"User-Agent": "requests/2.19.1"}), indent=4))
    print(json.dumps(headers({"Host": "www.biquge5200.cc", "Referer": "www.biquge5200.cc"}), indent=4))
