"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

GET、POST、PUT、DELETE、HEAD、OPTIONS、PATCH
"""
import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/get") as resp:
            assert resp.status == 200
        async with session.post("http://httpbin.org/post", data=b'data') as resp:
            assert resp.status == 200
        async with session.put("http://httpbin.org/put", data=b'data') as resp:
            assert resp.status == 200
        async with session.delete("http://httpbin.org/delete") as resp:
            assert resp.status == 200
        async with session.head("http://httpbin.org/get") as resp:
            assert resp.status == 200
        async with session.options("http://httpbin.org/get") as resp:
            assert resp.status == 200
        async with session.patch("http://httpbin.org/patch", data=b'data') as resp:
            assert resp.status == 200


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
