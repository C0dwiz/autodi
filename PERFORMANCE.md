# AutoDI Performance Optimization Guide

## ⚡ Resolution Performance Metrics

### Benchmark Results (Python 3.10)
```text
| Operation               | Time (μs) | Memory (KB) |
|-------------------------|----------|------------|
| Simple Resolution       | 45.2     | 2.1        |
| Deep Chain (5 levels)   | 128.7    | 6.8        |
| Singleton Resolution    | 12.4     | 0.3        |
| Async Resolution        | 89.5     | 3.2        |
```

## 🚀 Startup Optimization

### Eager Initialization
```python
@app.on_event("startup")
async def warmup_container():
    # Pre-resolve critical singletons
    container.resolve(DatabaseConnection)
    container.resolve(CacheService)
```

### Lazy Loading Pattern
```python
@inject(container, lazy=True)
class HeavyService:
    def __init__(self):
        self._loaded = False
    
    def _load(self):
        if not self._loaded:
            # Expensive initialization
            self._loaded = True

    def operation(self):
        self._load()
        # ... normal operations
```

## 🧠 Memory Management

### Singleton vs Transient
```python
# Memory-efficient singleton
container.register(AnalyticsService, is_singleton=True)

# Lightweight transient
container.register(RequestValidator)
```

### Scoped Dependencies
```python
# Request-scoped (FastAPI)
@app.middleware("http")
async def di_scope(request: Request, call_next):
    with container.scope("request"):
        response = await call_next(request)
        container.cleanup_scope("request")  # Release resources
    return response
```

## 🔄 Caching Strategies

### Resolution Cache
```python
# Enable resolution caching (reuses resolved graphs)
container.enable_resolution_cache()

# Clear between test cases
def teardown():
    container.clear_resolution_cache()
```

### Type Hint Cache
```python
# Pre-cache complex types
container.cache_type_hints(MyService)

# Disable for memory-constrained environments
container.disable_type_hint_caching()
```

## 🛠️ Production Configuration

### Recommended Settings
```python
container.configure(
    resolution_cache=True,  # ~15% faster resolution
    type_hint_cache=True,  # ~30% faster first resolution
    lazy_validation=False,  # Validate upfront
    strict_mode=True       # Fail fast on config errors
)
```

### Container Pooling
```python
from concurrent.futures import ThreadPoolExecutor

def worker():
    with container.clone() as thread_container:
        # Thread-safe operations
        service = thread_container.resolve(Service)
        service.process()

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(worker) for _ in range(10)]
```

## 📉 Performance Pitfalls

### Anti-Patterns to Avoid
```python
# ❌ Dynamic registration in hot paths
@app.get("/route")
def bad_route():
    container.register(NewType, lambda: ...)  # Expensive
    return container.resolve(NewType)

# ❌ Deep dependency chains
class A:
    def __init__(self, b: B, c: C, d: D, e: E): ...

# ❌ Excessive init hooks
@inject(container, init_hook="init1", secondary_hook="init2")
class OverloadedService: ...
```

## 🔧 Profiling Techniques

### Resolution Tracing
```python
# Generate flamegraph
with container.profile() as profiler:
    service = container.resolve(ComplexService)
    
profiler.export_flamegraph("resolution.svg")
```

### Memory Profiling
```python
from memory_profiler import profile

@profile
def test_memory_usage():
    container = Container()
    container.register(DataService)
    return container.resolve(DataService)
```

[← Back to Documentation](README.md) | [Testing Guide →](TESTING.md)