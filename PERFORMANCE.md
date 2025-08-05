# AutoDI Performance

AutoDI is designed to be lightweight and efficient, but as with any dependency injection framework, there are performance considerations to keep in mind.

## ⚡ Resolution Overhead

Dependency resolution is not free. Each time you resolve a dependency, the container performs a series of actions:

1.  **Lookup**: Finding the registered provider for the requested type.
2.  **Scope Check**: Verifying if the dependency is already created in the current scope.
3.  **Instantiation**: Calling the provider (factory) to create a new instance if one doesn't exist.
4.  **Lifecycle Hooks**: Calling `init_hook` if one is defined.

For most applications, this overhead is negligible. However, in performance-critical code paths, you should be mindful of how often you resolve new dependencies.

## 🧠 Memory Management

Understanding scopes is key to managing memory effectively.

-   **`Scope.APP` (Singleton)**: Use this for large, long-lived objects that are expensive to create. Since only one instance is ever created, it's memory-efficient. Be cautious about storing mutable state in singletons, as it will be shared across the entire application.

-   **`Scope.REQUEST`**: This scope is designed for short-lived objects. The memory used by these dependencies is reclaimed when the scope is exited. This is ideal for web requests or other transactional tasks.

## 🚀 Best Practices

### 1. Avoid Resolving in Hot Loops

Resolving dependencies inside a tight loop can add unnecessary overhead. If you need a dependency multiple times within the same block of code, resolve it once and reuse the instance.

```python
# Good: Resolve once outside the loop
service = container.resolve(MyService)
for item in items:
    service.process(item)

# Bad: Resolving repeatedly inside the loop
for item in items:
    service = container.resolve(MyService)
    service.process(item)
```

### 2. Use Scopes Correctly

Placing a dependency in the correct scope is the most important performance optimization you can make. Assigning a dependency to `Scope.APP` when it could be `Scope.REQUEST` might hold onto memory unnecessarily.

### 3. Keep Providers Fast

Your provider functions (factories) should be fast and efficient. Avoid performing heavy I/O or blocking operations directly within a provider. If a dependency needs to perform a slow initialization, use the `init_hook` to do it asynchronously.

[← Back to Documentation](README.md) | [Testing Guide →](TESTING.md)
