#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import asyncio
import logging

import aiohttp

default_headers = {
    "Host": "www.biquge5200.cc",
    "Referer": "https://www.biquge5200.cc"
}


async def download(session, url, headers={}, error_url_queue=None):
    """
    HTTP下载函数，下载失败后会重试三次（重试间隔1秒）

    :param session: 下载客户端会话
    :param url: 下载URL地址
    :param headers: 请求消息头
    :param error_url_queue: 失败URL队列，如果指定该参数则不直接重试，而是将失败的URL添加到该队列，该队列值必须是：asyncio.Queue对象
    :return: 返回下载文档内容
    """
    headers.update(default_headers)

    for i in range(4):
        try:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.text()
        except aiohttp.ClientError:
            logging.error("下载 {} 出错！".format(url))
            # 如果队列非空，将URL添加到队列
            if error_url_queue is not None:
                await error_url_queue.put(url)
                return None
            else:
                await asyncio.sleep(i / 10)


async def testing():
    """
    测试函数

    :return:
    """
    async with aiohttp.ClientSession() as session:
        # 下载章节列表
        print("============================== 章节列表 ==============================")
        print(await download(session, "https://www.biquge5200.cc/52_52542/"))
        # 下载章节正文
        print("============================== 章节正文 ==============================")
        print(await download(session, "https://www.biquge5200.cc/52_52542/20380548.html"))
        # 下载错误网页
        print("============================== 错误网页 ==============================")
        queue = asyncio.Queue(16)
        print(await download(session, "https://zlikun.com/404", error_url_queue=queue))
        await queue.put(None)  # 当任务执行完成后，添加一个结束标记
        while True:
            data = await queue.get()
            if data is None:
                break
            else:
                print("失败URL：{}".format(data))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()
