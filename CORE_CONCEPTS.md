# AutoDI Core Concepts

## 🌟 Dependency Injection Basics

### What is DI?
Dependency Injection (DI) is a design pattern where objects receive their dependencies from an external source rather than creating them directly.

```python
# Without DI
class UserService:
    def __init__(self):
        self.db = Database()  # Direct dependency

# With DI
class UserService:
    def __init__(self, db: Database):  # Injected dependency
        self.db = db
```

## 🔧 Container Fundamentals

### Registration Types
| Type          | Description                          | Example                      |
|---------------|--------------------------------------|------------------------------|
| Interface     | Abstract type to implementation      | `register(Database, PostgresDB)` |
| Self-binding  | Class registers itself               | `register(UserService)`       |
| Factory       | Function that creates dependencies   | `register(str, create_config)`|

### Resolution Methods
```python
# Explicit resolution
service = container.resolve(UserService)

# Implicit (via type hints)
@inject(container)
class Controller:
    def __init__(self, service: UserService):  # Auto-resolved
        self.service = service
```

## ⚡ Lifetime Management

### Supported Lifetimes
1. **Transient** - New instance each time (default)
   ```python
   container.register(Service)
   ```

2. **Singleton** - Single shared instance
   ```python
   container.register(Service, is_singleton=True)
   ```

3. **Scoped** (Request-based) - Per-request instance
   ```python
   container.register(Service, scope="request")
   ```

## 🧩 Component Lifecycle

### Hooks System
```python
class ResourceService:
    def initialize(self):  # Init hook
        self.setup()
    
    def cleanup(self):     # Destroy hook
        self.release()

container.register(
    ResourceService,
    init_hook="initialize",
    destroy_hook="cleanup"
)
```

## 🔄 Dependency Graphs

### Complex Resolution
AutoDI automatically resolves dependency chains:
```
Controller → UserService → Database → Config
```

### Circular Dependencies
```python
class ServiceA:
    def __init__(self, b: 'ServiceB'): ...

class ServiceB:
    def __init__(self, a: ServiceA): ...

# Raises CircularDependencyError
container.resolve(ServiceA)
```

## 🛡️ Error Handling

### Common Exceptions
| Exception                     | Trigger Condition               |
|-------------------------------|---------------------------------|
| `DependencyResolutionError`   | Can't resolve dependency        |
| `CircularDependencyError`     | Circular reference detected     |
| `AsyncDependencyError`        | Async resolution failed         |

## 🧪 Testing Support

### Mocking Example
```python
class MockDatabase(Database):
    def query(self):
        return "mock_data"

def test_service():
    with container.override(Database, MockDatabase):
        service = container.resolve(UserService)
        assert service.get() == "mock_data"
```

## 📈 Best Practices

### Do's and Don'ts
✅ **Do**:
- Use constructor injection
- Leverage type hints
- Register interfaces not implementations

❌ **Don't**:
- Use service locator pattern
- Manually resolve deep in call stack
- Mix DI with direct instantiation

[← Back to Documentation](README.md)