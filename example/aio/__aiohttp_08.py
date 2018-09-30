"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#timeouts

timeout
"""

import asyncio

import aiohttp


async def main():
    # 请求超时时间，可以创建请求客户端时设置，也可以在请求时设置
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get("http://httpbin.org/get", timeout=timeout) as resp:
            assert resp.status == 200
            print(await resp.json(encoding="utf-8"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
