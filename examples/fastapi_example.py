from fastapi import FastAPI, Depends
from autodi import Container, inject

app = FastAPI()
container = Container()


class UserService:
    def get_users(self):
        return ["Alice", "Bob"]


container.register(UserService, UserService)


# Option 1: Explicitly creating a dependency
def get_user_service() -> UserService:
    return container.resolve(UserService)


@app.get("/users")
async def get_users(service: UserService = Depends(get_user_service)):
    return {"users": service.get_users()}


# Option 2: Using a lambda with a type annotation
@app.get("/users-lambda")
async def get_users_lambda(
    service: UserService = Depends(lambda: container.resolve(UserService)),
):
    return {"users": service.get_users()}


# Option 3: Using the @inject decorator (preferred way)
@app.get("/users-inject")
@inject(container)
async def get_users_inject(service: UserService):
    return {"users": service.get_users()}


# run: uvicorn fastapi_example:app --reload
