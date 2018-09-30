"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content

请求二进制文件，比如图片
"""

import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        async with session.get('https://api.github.com/events') as resp:
            print(await resp.content.read(10))

        async with session.get("https://www.baidu.com/img/bd_logo1.png") as resp:
            chunk_size = 16
            with open(r'../data/bd_logo.png', 'wb') as f:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
