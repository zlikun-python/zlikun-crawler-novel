"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#more-complicated-post-requests
https://docs.aiohttp.org/en/stable/client_quickstart.html#post-a-multipart-encoded-file
https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-uploads
https://docs.aiohttp.org/en/stable/multipart.html#aiohttp-multipart

复杂POST请求，含文件上传
"""

import asyncio

import aiohttp
from aiohttp import FormData


async def main():
    async with aiohttp.ClientSession() as session:
        payload = {'key1': 'value1', 'key2': 'value2'}
        async with session.post('http://httpbin.org/post', data=payload) as resp:
            # 'form': {'key1': 'value1', 'key2': 'value2'}
            print(await resp.json())
        async with session.post('http://httpbin.org/post', data=b'\x00Binary-data\x00') as resp:
            # 'data': '\x00Binary-data\x00'
            print(await resp.json())
        async with session.post('http://httpbin.org/post', json=payload) as resp:
            #  'data': '{"key1": "value1", "key2": "value2"}'
            print(await resp.json())
        async with session.post('http://httpbin.org/post', data="Hello") as resp:
            # 'data': 'Hello'
            print(await resp.json())

    async with aiohttp.ClientSession() as session:
        # 文件上传
        # https://docs.aiohttp.org/en/stable/client_quickstart.html#post-a-multipart-encoded-file
        data = FormData()
        data.add_field("file", open('../data/bd_logo.png', 'rb'), filename="logo.png", content_type="image/png")
        async with session.post("http://httpbin.org/post", data=data) as resp:
            print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
