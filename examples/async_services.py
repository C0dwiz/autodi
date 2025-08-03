import asyncio
from autodi import Container

container = Container()


class AsyncDataLoader:
    async def load_data(self):
        await asyncio.sleep(0.1)
        return [1, 2, 3]


async def main():
    loader = await container.resolve_async(AsyncDataLoader)
    data = await loader.load_data()
    print(data)  # [1, 2, 3]


# asyncio.run(main())
