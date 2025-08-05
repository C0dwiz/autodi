# AutoDI: Elegant Dependency Injection for Python

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**AutoDI** is a modern, type-friendly dependency injection container that simplifies dependency management in Python applications while keeping your code clean and maintainable.

## ✨ Features

- **Type-Safe Resolution**: Leverages type hints, including `NewType`, for resolving dependencies.
- **Flexible Scopes**: Manages dependency lifecycles with `APP` (singleton) and `REQUEST` scopes.
- **Lifecycle Hooks**: Automates resource management with `init_hook` and `destroy_hook`.
- **Full Async Support**: Seamlessly handles `async` providers and lifecycle hooks.
- **Test-Friendly**: Provides `override_provider` for easy mocking and test isolation.
- **Framework Integrations**: Offers helpers for frameworks like FastAPI.

## 📦 Installation

```bash
pip install git+https://github.com/C0dwiz/autodi
```

## 🚀 Quick Start

### Basic Usage

```python
from autodi import Container, Scope

# 1. Define your components
class Database:
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"

class UserService:
    def __init__(self, db: Database):
        self.db = db

# 2. Create and configure the container
container = Container()
container.register(Database, scope=Scope.APP) # Singleton
container.register(UserService, scope=Scope.REQUEST) # Per-request

# 3. Resolve dependencies
with container.enter_scope(Scope.REQUEST):
    service = container.resolve(UserService)
    print(service.db.query("SELECT * FROM users"))
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from autodi import Container, Scope
from autodi.extensions.fastapi import setup_dependency_injection

app = FastAPI()
container = Container()

# This middleware handles REQUEST scope creation and cleanup
setup_dependency_injection(app, container)

class AuthService:
    def login(self, user: str) -> str:
        return f"Welcome {user}!"

container.register(AuthService, scope=Scope.REQUEST)

@app.get("/login/{user}")
async def login(user: str, auth: AuthService = Depends(container.resolve_async)):
    return {"message": auth.login(user)}
```

## 🛠️ Advanced Features

### Lifecycle Hooks

Manage resources like database connections automatically.

```python
class DatabaseConnection:
    async def connect(self):
        print("Connecting to DB...")

    async def close(self):
        print("Closing DB connection...")

container.register(
    DatabaseConnection,
    scope=Scope.REQUEST,
    init_hook="connect",
    destroy_hook="close",
)

# `connect` is called on resolve, `close` is called when the scope ends.
async with container.enter_scope_async(Scope.REQUEST):
    db = await container.resolve_async(DatabaseConnection)
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
