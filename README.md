# AutoDI: Elegant Dependency Injection for Python

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**AutoDI** is a modern, type-friendly dependency injection container that simplifies dependency management in Python applications while keeping your code clean and maintainable.

## ✨ Features

- **Zero Configuration** for basic usage
- **Type Annotations Support** for intuitive dependency resolution
- **Singleton & Transient Lifetimes** out of the box
- **Lifecycle Hooks** for resource management
- **Async Support** for modern Python apps
- **Test-Friendly** with easy mock integration
- **FastAPI/Aiogram** first-class support

## 📦 Installation

```bash
pip install git+https://github.com/C0dwiz/autodi
```

## 🚀 Quick Start

### Basic Usage

```python
from autodi import Container

container = Container()

class Database:
    def connect(self):
        return "Connected!"

class UserService:
    def __init__(self, db: Database):  # Auto-injected
        self.db = db

service = container.resolve(UserService)
print(service.db.connect())  # "Connected!"
```

### FastAPI Integration

```python
from fastapi import FastAPI
from autodi import Container, inject

app = FastAPI()
container = Container()

@inject(container)
class AuthService:
    def login(self, user: str):
        return f"Welcome {user}!"

@app.get("/login/{user}")
async def login(user: str, auth: AuthService):
    return {"message": auth.login(user)}
```

## 🛠️ Advanced Features

### Lifecycle Hooks

```python
class CacheService:
    def __init__(self):
        self._cache = {}
    
    def init_cache(self):  # Init hook
        self._cache.update(preload_data())
    
    def cleanup(self):     # Destroy hook
        self._cache.clear()

container.register(
    CacheService,
    init_hook="init_cache",
    destroy_hook="cleanup",
    is_singleton=True
)
```

### Async Dependencies

```python
class AsyncLoader:
    async def load_data(self):
        await asyncio.sleep(0.1)
        return [1, 2, 3]

async def main():
    loader = await container.resolve_async(AsyncLoader)
    data = await loader.load_data()
```

## 📚 Documentation

Explore our comprehensive guides:

- [Core Concepts](CORE_CONCEPTS.md)
- [Framework Integrations](FRAMEWORKS.md)
- [Testing Strategies](TESTING.md)
- [Performance Tips](PERFORMANCE.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md).

## 📜 License

MIT © 2023 AutoDI Team