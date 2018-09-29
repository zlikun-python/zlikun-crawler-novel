"""
https://docs.aiohttp.org/en/stable/client_quickstart.html#response-content-and-status-code
https://docs.aiohttp.org/en/stable/client_quickstart.html#binary-response-content
https://docs.aiohttp.org/en/stable/client_quickstart.html#json-request
https://docs.aiohttp.org/en/stable/client_quickstart.html#json-response-content

响应正文及状态码
"""
import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # GET
        async with session.get("http://httpbin.org/get") as resp:
            assert resp.status == 200
            # 获取文本类型响应信息
            print(await resp.text(encoding="utf-8"))
            # 获取JSON类型响应信息
            print(await resp.json(encoding="utf-8"))
            # 获取二进制响应信息
            print(await resp.read())

        # POST，请求参数为JSON类型
        async with session.post("http://httpbin.org/post", json={"name": "张三"}) as resp:
            assert resp.status == 200
            print(await resp.json())

    # # ujson库是一个第三方json库，性能要比标准json库要好（在windows环境下测试时，安装失败）
    # # https://pypi.org/project/ujson/
    # async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
    #     async with session.post("http://httpbin.org/post", json={"name": "张三"}) as resp:
    #         assert resp.status == 200
    #         print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
