"""
https://docs.aiohttp.org/en/stable/

GET 请求、响应对象属性清单
"""
import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as response:
            print(response.method)  # GET
            print(response.status)  # 200
            print(response.reason)  # OK
            print(response.charset)  # None
            print(response.links)  # <MultiDictProxy()>
            print(response.content_type)  # application/json
            print(response.content_length)  # 270
            print(response.content)  # <StreamReader 270 bytes eof>
            print(response.cookies)  #
            print(response.host)  # httpbin.org
            # ((b'Connection', b'keep-alive'), (b'Server', b'gunicorn/19.9.0'), (b'Date', b'Sat, 29 Sep 2018 05:43:03 GMT'), (b'Content-Type', b'application/json'), (b'Content-Length', b'270'), (b'Access-Control-Allow-Origin', b'*'), (b'Access-Control-Allow-Credentials', b'true'), (b'Via', b'1.1 vegur'))
            print(response.raw_headers)
            print(response.real_url)  # https://httpbin.org/get
            print(response.url)  # https://httpbin.org/get
            print(response.content_disposition)  # None
            print(response.get_encoding())  # utf-8
            print(response.history)  # ()
            response.raise_for_status()
            # {'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Host': 'httpbin.org', 'User-Agent': 'Python/3.7 aiohttp/3.4.4'}, 'origin': '116.228.16.198', 'url': 'https://httpbin.org/get'}
            print(await response.json(encoding='utf-8'))
            # {
            #   "args": {},
            #   "headers": {
            #     "Accept": "*/*",
            #     "Accept-Encoding": "gzip, deflate",
            #     "Connection": "close",
            #     "Host": "httpbin.org",
            #     "User-Agent": "Python/3.7 aiohttp/3.4.4"
            #   },
            #   "origin": "116.228.16.198",
            #   "url": "https://httpbin.org/get"
            # }
            print(await response.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
