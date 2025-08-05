# AutoDI Core Concepts

## 🌟 Dependency Injection Basics

### What is DI?
Dependency Injection (DI) is a design pattern where objects receive their dependencies from an external source (the "container") rather than creating them directly. This decouples your components, making them more modular, testable, and maintainable.

```python
# Without DI
class UserService:
    def __init__(self):
        self.db = Database()  # Direct, tight coupling

# With DI
class UserService:
    def __init__(self, db: Database):  # Injected, loose coupling
        self.db = db
```

## 🔧 Container Fundamentals

The `Container` is the central component of AutoDI. It is responsible for managing the registration and resolution of your dependencies.

### Registration
You register a dependency by telling the container how to create it and what its lifecycle should be.

```python
# Register a class. The container will instantiate it.
container.register(UserService, scope=Scope.REQUEST)

# Register a provider (factory function) for more complex creation.
container.register(Database, provider=create_db_connection, scope=Scope.APP)
```

### Resolution
You resolve a dependency by asking the container for an instance of a specific type.

```python
# Explicitly resolve an instance
service = container.resolve(UserService)

# The container automatically resolves dependencies for other dependencies.
# When resolving UserService, the container sees it needs a Database and resolves it first.
```

## ⚡ Scope Management

A dependency's "scope" defines its lifecycle: how long an instance should live.

1.  **`Scope.APP`** (Singleton)
    - A single instance is created and shared for the entire lifecycle of the container.
    - Use for objects that are expensive to create and stateless, like database connection pools or configuration objects.
    ```python
    container.register(Config, scope=Scope.APP)
    ```

2.  **`Scope.REQUEST`** (Scoped)
    - A new instance is created for each scope block (e.g., a web request or a worker task) and destroyed when the scope exits.
    - This is the default for unregistered dependencies.
    - Use for objects that hold request-specific state, like database sessions or user-specific services.
    ```python
    with container.enter_scope(Scope.REQUEST):
        service = container.resolve(RequestScopedService)
    # `service` is now destroyed
    ```

## 🧩 Component Lifecycle Hooks

AutoDI can manage resources that need explicit setup and teardown, like network connections or file handles.

-   `init_hook`: The name of a method to be called *after* the instance is created.
-   `destroy_hook`: The name of a method to be called when the instance's scope is destroyed.

```python
class MessageQueue:
    def connect(self): ...
    def close(self): ...

container.register(
    MessageQueue,
    scope=Scope.APP,
    init_hook="connect",
    destroy_hook="close"
)

# When the app shuts down...
container.cleanup() # This will call the `close` method.
```

## 🔄 Dependency Graphs

AutoDI automatically resolves entire dependency chains. If `ControllerA` depends on `ServiceB`, and `ServiceB` depends on `DatabaseC`, the container handles the instantiation of all three in the correct order.

### Circular Dependencies
AutoDI will detect circular dependencies (e.g., A depends on B, and B depends on A) and raise a `CircularDependencyError` to prevent infinite recursion.

## 🛡️ Error Handling

| Exception                 | When It's Raised                               |
| ------------------------- | ---------------------------------------------- |
| `DependencyResolutionError` | A dependency is requested but not registered.  |
| `CircularDependencyError` | A circular reference is detected.              |
| `ScopeError`              | A scope mismatch occurs (e.g., nested scopes). |
| `ProviderError`           | A provider function fails during execution.    |

[← Back to Documentation](README.md)
