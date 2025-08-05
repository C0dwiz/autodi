# AutoDI Framework Integrations

AutoDI is designed to integrate smoothly with popular Python web frameworks. Here are some recommended patterns.

## 🚀 FastAPI Integration

FastAPI's dependency injection system works seamlessly with AutoDI.

### Recommended Setup

This pattern uses a middleware to manage the `REQUEST` scope and a simple helper to inject dependencies.

```python
# main.py
from fastapi import FastAPI, Depends
from autodi import Container, Scope
from autodi.extensions.fastapi import setup_dependency_injection

app = FastAPI()
container = Container()

# This middleware automatically creates and cleans up the REQUEST scope.
setup_dependency_injection(app, container)

# --- Define and register your dependencies ---

class MyService:
    def do_work(self) -> str:
        return "Work done!"

container.register(MyService, scope=Scope.REQUEST)

# --- Inject into your endpoints ---

@app.get("/")
async def read_root(service: MyService = Depends(container.resolve_async)):
    return {"message": service.do_work()}
```

### Lifecycle Management with FastAPI

Use lifecycle hooks for resources that need to be managed per-request.

```python
class DatabaseConnection:
    async def connect(self): ...
    async def close(self): ...

container.register(
    DatabaseConnection,
    scope=Scope.REQUEST,
    init_hook="connect",
    destroy_hook="close",
)

# The `setup_dependency_injection` middleware ensures that `connect` is called
# at the beginning of a request and `close` is called at the end.
```

## 🤖 Aiogram (Telegram Bot) Integration

Use a custom middleware to manage scopes for each incoming message or event.

### Recommended Setup

```python
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from autodi import Container, Scope

class DiMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    async def __call__(self, handler, event, data):
        async with self.container.enter_scope_async(Scope.REQUEST):
            data["container"] = self.container
            return await handler(event, data)

# --- In your main setup ---
dp = Dispatcher()
dp.update.outer_middleware.register(DiMiddleware(container))

# --- In your handlers ---

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, container: Container):
    service = await container.resolve_async(MyService)
    await message.answer(service.get_reply())
```

[← Back to Documentation](README.md) | [Core Concepts →](CORE_CONCEPTS.md)
