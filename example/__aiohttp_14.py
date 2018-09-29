"""
https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support

Proxy
"""

import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as client:
        # 普通代理
        async with client.get('https://httpbin.org/ip', proxy='https://114.225.169.214:53128') as resp:
            print(await resp.json())

        # # 代理认证
        # proxy_auth = aiohttp.BasicAuth('user', 'pass')
        # async with client.get('https://httpbin.org/ip', proxy='', proxy_auth=proxy_auth) as resp:
        #     print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
