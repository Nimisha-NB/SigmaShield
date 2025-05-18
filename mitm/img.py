import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def run_in_executor(self, func, *args):
    return await asyncio.get_event_loop().run_in_executor(executor, lambda: asyncio.run(func(*args)))

async def my_async_task(self, url: str):
    await asyncio.sleep(5)  # Simulate long-running task
    return f"Processed: {url}"