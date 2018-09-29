"""
https://docs.aiohttp.org/en/stable/client_advanced.html#client-tracing

客户端请求追溯
"""

import asyncio

import aiohttp


async def main():
    async def on_request_start(
            session, trace_config_ctx, params):
        print("Starting request: {}, {}, {}".format(session, trace_config_ctx, params))

    async def on_request_end(session, trace_config_ctx, params):
        print("Ending request: {}, {}, {}".format(session, trace_config_ctx, params))

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    async with aiohttp.ClientSession(trace_configs=[trace_config]) as client:
        async with client.get('http://httpbin.org/ip') as resp:
            print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
