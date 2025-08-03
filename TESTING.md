# AutoDI Testing Guide

## 🧪 Unit Testing Fundamentals

### Basic Test Setup
```python
import pytest
from autodi import Container

class TestService:
    def process(self):
        return "Real result"

def test_basic_resolution():
    container = Container()
    container.register(TestService)
    
    service = container.resolve(TestService)
    assert service.process() == "Real result"
```

### Mocking Dependencies
```python
from unittest.mock import Mock

def test_with_mocks():
    container = Container()
    
    # Create and register mock
    mock_db = Mock()
    mock_db.query.return_value = "test_data"
    container.register(Database, mock_db)
    
    service = container.resolve(UserService)
    assert service.get_data() == "test_data"
```

## 🎯 Advanced Testing Patterns

### Contextual Mocks
```python
class TestPaymentService:
    def test_declined_payments(self):
        container = Container()
        
        # Override only for this test
        with container.override(PaymentGateway, DeclinedPaymentMock):
            service = container.resolve(OrderService)
            result = service.process_payment(100)
            
            assert result.status == "declined"
```

### Pytest Fixtures
```python
import pytest

@pytest.fixture
def di_container():
    container = Container()
    container.register(AuthService)
    yield container
    container.cleanup()  # Call destroy hooks

def test_auth_service(di_container):
    service = di_container.resolve(AuthService)
    assert service.login("admin") is True
```

## 🚦 Integration Testing

### Testing with Real Container
```python
def test_full_workflow():
    # Configure container as in production
    container = configure_prod_container()
    
    # Replace just one external service
    container.register(EmailService, MockEmailService)
    
    # Test complete flow
    result = container.resolve(MainWorkflow).run()
    assert result.success is True
```

### Async Service Testing
```python
@pytest.mark.asyncio
async def test_async_service():
    container = Container()
    container.register(AsyncDataLoader)
    
    loader = await container.resolve_async(AsyncDataLoader)
    data = await loader.load()
    assert len(data) > 0
```

## 🔄 Dependency Isolation

### Resetting State Between Tests
```python
@pytest.fixture(autouse=True)
def reset_container():
    Container._global_instance = None  # Reset singleton container
    yield
```

### Testing Circular Dependencies
```python
def test_circular_deps():
    container = Container()
    
    class ServiceA:
        def __init__(self, b: 'ServiceB'): ...
    
    class ServiceB:
        def __init__(self, a: ServiceA): ...
    
    with pytest.raises(CircularDependencyError):
        container.resolve(ServiceA)
```

## 🛠️ Debugging Techniques

### Resolution Tracing
```python
def test_debug_resolution():
    container = Container()
    container.trace_resolution = True  # Enable debug logs
    
    # Test will output resolution path:
    # Resolving UserService → Database → Config
    container.resolve(UserService)
```

### Dependency Graph Validation
```python
def test_dependency_graph():
    container = configure_prod_container()
    graph = container.get_dependency_graph()
    
    # Verify no unexpected dependencies
    assert "ObsoleteService" not in graph
    assert "Database" in graph["UserService"]
```

## 📊 Test Coverage Strategies

### Key Areas to Test
1. **Container Registration**
   ```python
   def test_registration():
       container = Container()
       container.register(Interface, Implementation)
       assert container.is_registered(Interface) is True
   ```

2. **Lifecycle Hooks**
   ```python
   def test_init_hook():
       mock = Mock()
       container.register(Service, init_hook="setup")
       container.resolve(Service)
       mock.setup.assert_called_once()
   ```

3. **Edge Cases**
   ```python
   def test_unregistered_service():
       container = Container()
       with pytest.raises(DependencyResolutionError):
           container.resolve(UnregisteredService)
   ```

[← Back to Documentation](README.md) | [Framework Integrations →](FRAMEWORKS.md)