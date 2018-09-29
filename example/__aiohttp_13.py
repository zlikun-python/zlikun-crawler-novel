"""
https://docs.aiohttp.org/en/stable/client_advanced.html#ssl-control-for-tcp-sockets

HTTPS
"""

import asyncio
import ssl

import aiohttp


async def main():
    # 不验证SSL
    async with aiohttp.ClientSession() as client:
        async with client.get('https://httpbin.org/ip', ssl=False) as resp:
            print(await resp.json())

    # 验证SSL
    ssl_context = ssl.create_default_context(cafile='/path/to/ca-bundle.crt')
    # verify self-signed certificates
    ssl_context.load_cert_chain('/path/to/client/public/device.pem', '/path/to/client/private/device.key')
    async with aiohttp.ClientSession() as client:
        try:
            async with client.get('https://httpbin.org/ip', ssl=ssl_context) as resp:
                print(await resp.json())
        except aiohttp.ClientConnectorSSLError as e:
            assert isinstance(e, ssl.SSLError)
        except aiohttp.ClientConnectorCertificateError as e:
            assert isinstance(e, ssl.CertificateError)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
