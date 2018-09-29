"""
https://docs.aiohttp.org/en/stable/client_advanced.html#client-session
https://docs.aiohttp.org/en/stable/client_advanced.html#custom-request-headers
https://docs.aiohttp.org/en/stable/client_advanced.html#custom-cookies
https://docs.aiohttp.org/en/stable/client_advanced.html#response-headers-and-cookies
https://docs.aiohttp.org/en/stable/client_advanced.html#cookie-jar
https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.cookie_jar

定制请求、响应消息头和Cookie
"""

import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        # 定制请求消息头
        async with session.get("http://httpbin.org/headers", headers={
            "User-Agent": "zlikun & aiohttp/3.4.4"
        }) as resp:
            # 请求消息头
            json_body = await resp.json()
            print(json_body['headers'])
            # 响应消息头
            print(resp.headers)

    # 定制cookie
    url = 'http://httpbin.org/cookies'
    cookies = {'cookies_are': 'working'}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url) as resp:
            json_body = await resp.json()
            # 请求cookies
            # {'cookies_are': 'working'}
            print(json_body['cookies'])
            # 响应cookies
            print(resp.cookies)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
