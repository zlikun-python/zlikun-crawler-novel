"""
https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown

Graceful Shutdown
"""

import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as client:
        async with client.get('https://httpbin.org/ip') as resp:
            print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.75))
    loop.close()
