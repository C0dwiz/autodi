# AutoDI Framework Integrations

## 🚀 FastAPI Integration

### Basic Setup
```python
from fastapi import FastAPI, Depends
from autodi import Container

app = FastAPI()
container = Container()

class AuthService:
    def login(self, username: str):
        return f"Welcome {username}!"

# Option 1: Direct resolution
@app.get("/login")
async def login(username: str):
    service = container.resolve(AuthService)
    return service.login(username)

# Option 2: Using Depends
@app.get("/login-depends")
async def login_depends(
    username: str,
    service: AuthService = Depends(container.resolve(AuthService))
):
    return service.login(username)
```

### Advanced Pattern (Recommended)
```python
from autodi import inject

@inject(container)
class PaymentService:
    def charge(self, amount: float):
        return f"Charged ${amount:.2f}"

@app.post("/payments")
async def create_payment(
    amount: float,
    service: PaymentService  # Auto-injected
):
    return {"result": service.charge(amount)}
```

## 🤖 Aiogram (Telegram Bot) Integration

### Handler Injection
```python
from aiogram import Dispatcher, types
from autodi import inject

dp = Dispatcher(bot)

@inject(container)
class MessageHandler:
    def __init__(self, analytics: AnalyticsService):
        self.analytics = analytics
    
    async def handle_message(self, message: types.Message):
        await self.analytics.track(message)
        return "Processed!"

@dp.message_handler()
async def on_message(
    message: types.Message,
    handler: MessageHandler  # Auto-injected
):
    await handler.handle_message(message)
```

### Factory Pattern
```python
class NotificationService:
    async def send(self, user_id: int, text: str):
        ...

def create_service() -> NotificationService:
    return NotificationService()

container.register(NotificationService, create_service)

@dp.message_handler(commands=['notify'])
async def notify_user(
    message: types.Message,
    service: NotificationService = Depends(container.resolve(NotificationService))
):
    await service.send(message.from_user.id, "Hello!")
```

## 🌐 Django Integration

### services.py
```python
from autodi import container

class EmailService:
    def send(self, to: str, body: str):
        ...

container.register(EmailService)
```

### views.py
```python
from django.http import JsonResponse
from .services import container

def send_email_view(request):
    service = container.resolve(EmailService)
    service.send("user@example.com", "Hello Django!")
    return JsonResponse({"status": "sent"})
```

### Custom Middleware
```python
class DIContainerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request.container = container  # Attach to request
        return self.get_response(request)
```

## 🔥 Flask Integration

### Application Factory
```python
from flask import Flask
from autodi import Container

def create_app():
    app = Flask(__name__)
    di = Container()
    
    @app.route("/")
    def index():
        service = di.resolve(SomeService)
        return service.process()
    
    return app
```

### Blueprint Example
```python
@inject(container)
class ReportService:
    def generate(self):
        return "Report data"

bp = Blueprint('reports', __name__)

@bp.route("/report")
def get_report(service: ReportService):  # Injected
    return service.generate()
```

## ⚡ Performance Tips

### Framework-Specific Optimizations
1. **FastAPI**: Pre-resolve dependencies in startup events
   ```python
   @app.on_event("startup")
   async def setup_di():
       container.resolve(SingletonService)  # Warm-up
   ```

2. **Aiogram**: Use middleware for request-scoped dependencies
   ```python
   class DIMiddleware(BaseMiddleware):
       async def __call__(self, handler, event, data):
           data['di_container'] = container
           return await handler(event, data)
   ```

3. **Django/Flask**: Cache container in app config
   ```python
   app.extensions['di'] = container
   ```

[← Back to Documentation](README.md) | [Core Concepts →](CORE_CONCEPTS.md)