import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from autodi import Container, Scope

# --- Define Dependencies ---

class GreetingService:
    """A simple service to generate greetings."""
    def get_greeting(self, name: str) -> str:
        """Generates a greeting string.

        Args:
            name: The name to greet.

        Returns:
            A greeting string.
        """
        return f"Hello, {name}!"


class UserService:
    """A service that depends on GreetingService."""
    def __init__(self, greeting_service: GreetingService):
        """Initializes the UserService.

        Args:
            greeting_service: An instance of GreetingService.
        """
        self._greeting_service = greeting_service

    def greet_user(self, user_id: int, name: str) -> str:
        """Greets a user by their ID and name.

        Args:
            user_id: The user's ID.
            name: The user's name.

        Returns:
            A greeting string for the user.
        """
        print(f"Greeting user {user_id}")
        return self._greeting_service.get_greeting(name)

# --- Configure Container ---

container = Container()

# Register services
container.register(GreetingService, scope=Scope.APP)  # Singleton, lives for the whole app
container.register(UserService, scope=Scope.REQUEST) # Created for each incoming message

# --- Setup Aiogram ---

# In a real app, the token should be loaded from a secure source
# bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()


class DiMiddleware(BaseMiddleware):
    """Middleware to manage dependency scopes for each incoming update."""
    def __init__(self, container: Container):
        """Initializes the DiMiddleware.

        Args:
            container: The autodi container instance.
        """
        self.container = container

    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], event: Message, data: dict
    ) -> Any:
        """Enters an async scope and resolves dependencies for the handler.

        Args:
            handler: The next handler in the chain.
            event: The incoming event (Message).
            data: The data to be passed to the handler.

        Returns:
            The result of the handler.
        """
        async with self.container.enter_scope_async(Scope.REQUEST):
            data["user_service"] = await self.container.resolve_async(UserService)
            return await handler(event, data)

dp.update.outer_middleware.register(DiMiddleware(container))


@dp.message(CommandStart())
async def start_handler(message: Message, user_service: UserService):
    """Handler for the /start command."""
    user = message.from_user
    greeting = user_service.greet_user(user.id, user.full_name) # type: ignore
    await message.answer(greeting)


async def main():
    """Main function to run the bot."""
    # To run this example:
    # 1. Uncomment the following line
    # 2. Replace "YOUR_TOKEN" with your actual bot token
    # await dp.start_polling(bot)
    print("Aiogram example updated. To run, set a bot token and uncomment start_polling.")


if __name__ == "__main__":
    asyncio.run(main())