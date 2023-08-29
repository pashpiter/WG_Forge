import aiohttp
import asyncio
import time


async def task(session):
    resp = await session.get('http://localhost:8080/ping')
    return resp.status


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [task(session) for i in range(1000)]
        t = time.perf_counter()
        r = await asyncio.gather(*tasks, return_exceptions=True)
        print(f'Всего - {len(r)}, ERR - {r.count(429)}, OK - {r.count(200)}')
        print(f'Time = {time.perf_counter() - t}')

asyncio.run(main())
