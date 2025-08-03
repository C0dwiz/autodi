from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from autodi import Container, inject

container = Container()
bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()


class UserManager:
    async def greet_user(self, user_id: int):
        return f"Hello, user {user_id}!"


container.register(UserManager, UserManager)


@dp.message(CommandStart())
@inject(container)
async def start_handler(message: Message, user_manager: UserManager):
    greeting = await user_manager.greet_user(message.from_user.id)  # type: ignore
    await message.answer(greeting)


async def main():
    await dp.start_polling()


# asyncio.run(main())
