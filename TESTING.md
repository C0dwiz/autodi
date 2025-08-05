# AutoDI Testing Guide

One of the primary benefits of dependency injection is improved testability. AutoDI provides tools to make testing your components easy and efficient.

## 🎯 Overriding Providers for Mocks

The most powerful feature for testing is the ability to replace a real dependency with a mock or fake version. This allows you to test components in isolation.

### Basic Mocking Example

```python
from unittest.mock import Mock
import pytest

# --- Your application code ---
class Database:
    def get_user(self, user_id: int) -> str:
        # ... interacts with a real database
        return "real_user"

class UserService:
    def __init__(self, db: Database):
        self.db = db

    def get_user_name(self, user_id: int) -> str:
        return self.db.get_user(user_id)

# --- Your test code ---

def test_user_service_with_mock():
    container = Container()
    container.register(UserService, scope=Scope.REQUEST)

    # Create a mock for the Database
    mock_db = Mock(spec=Database)
    mock_db.get_user.return_value = "mock_user"

    # Override the real Database provider with our mock
    container.override_provider(Database, provider=lambda: mock_db)

    with container.enter_scope(Scope.REQUEST):
        service = container.resolve(UserService)
        result = service.get_user_name(1)

        assert result == "mock_user"
        mock_db.get_user.assert_called_once_with(1)
```

## 🧪 Using Pytest Fixtures

For more complex applications, you can use `pytest` fixtures to set up and tear down your container and dependencies for each test.

```python
@pytest.fixture
def test_container() -> Container:
    container = Container()
    # You can register common test dependencies here
    return container

def test_some_feature(test_container: Container):
    # Override a specific dependency for this test
    test_container.override_provider(EmailService, provider=lambda: MockEmailService())

    with test_container.enter_scope(Scope.REQUEST):
        service = test_container.resolve(MyFeatureService)
        assert service.run() is True
```

## 🚦 Testing Asynchronous Services

Testing `async` components follows the same pattern, but uses `resolve_async` and `enter_scope_async`.

```python
@pytest.mark.asyncio
async def test_async_service_with_mock():
    container = Container()
    container.register(AsyncService, scope=Scope.REQUEST)

    mock_api = Mock()
    mock_api.fetch.return_value = asyncio.Future()
    mock_api.fetch.return_value.set_result("mock_data")

    container.override_provider(ExternalAPI, provider=lambda: mock_api)

    async with container.enter_scope_async(Scope.REQUEST):
        service = await container.resolve_async(AsyncService)
        result = await service.get_data()

        assert result == "mock_data"
```

## 🛡️ Testing for Errors

You can also test that your application correctly handles errors from the container, such as circular dependencies.

```python
def test_circular_dependency_detection():
    container = Container()

    class ServiceA:
        def __init__(self, b: 'ServiceB'): ...

    class ServiceB:
        def __init__(self, a: ServiceA): ...

    container.register(ServiceA)
    container.register(ServiceB)

    with pytest.raises(CircularDependencyError):
        container.resolve(ServiceA)
```

[← Back to Documentation](README.md) | [Framework Integrations →](FRAMEWORKS.md)
