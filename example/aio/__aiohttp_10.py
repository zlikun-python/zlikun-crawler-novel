"""
https://docs.aiohttp.org/en/stable/client_advanced.html#redirection-history

重定向历史
"""

import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.oschina.net/") as resp:
            # 返回重定向后网站信息（通常为200，这里为osc网站特殊定制实现，忽略之）
            assert resp.status == 403
            assert str(resp.url) == 'https://www.oschina.net/'
            assert len(resp.history) == 1
            assert resp.history[0].status == 301
            assert str(resp.history[0].url) == 'http://www.oschina.net/'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
