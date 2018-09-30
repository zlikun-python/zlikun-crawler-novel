"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#passing-parameters-in-urls

Get Query String
"""
import asyncio

import aiohttp
from yarl import URL


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/get", params={"key1": "value1", "key2": "value2"}) as resp:
            assert resp.status == 200
            # <class 'yarl.URL'> http://httpbin.org/get?key1=value1&key2=value2
            print(type(resp.url), resp.url)
            # <class 'yarl.URL'> http://httpbin.org/get?key1=value1&key2=value2
            print(type(resp.url), resp.real_url)
            print(await resp.text())
        async with session.get(URL("http://httpbin.org/get", encoded=True), params={"name": "张三"}) as resp:
            # <class 'yarl.URL'> http://httpbin.org/get?name=%E5%BC%A0%E4%B8%89
            print(type(resp.url), resp.url)
            # ...
            # "url": "http://httpbin.org/get?name=\u5f20\u4e09"
            # ...
            print(await resp.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
