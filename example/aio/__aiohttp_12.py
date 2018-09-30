"""
https://docs.aiohttp.org/en/stable/client_advanced.html#limiting-connection-pool-size
https://docs.aiohttp.org/en/stable/client_advanced.html#tuning-the-dns-cache
https://docs.aiohttp.org/en/stable/client_advanced.html#resolving-using-custom-nameservers
https://docs.aiohttp.org/en/stable/client_advanced.html#unix-domain-sockets

连接池、DNS
"""

import asyncio

import aiohttp


async def main():
    conn = aiohttp.TCPConnector(limit=5)
    # conn = aiohttp.TCPConnector(limit=0)
    # conn = aiohttp.TCPConnector(limit_per_host=30)
    # conn = aiohttp.TCPConnector(ttl_dns_cache=300)
    # conn = aiohttp.TCPConnector(use_dns_cache=False)
    # conn = aiohttp.UnixConnector(path='/path/to/socket')

    async with aiohttp.ClientSession(connector=conn) as client:
        for _ in range(8):
            async with client.get('http://httpbin.org/ip') as resp:
                print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
