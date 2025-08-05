from autodi import Container, Scope


class Database:
    """A dummy Database class."""

    def get_data(self) -> list[str]:
        return ["data1", "data2"]


class DataService:
    """A service that depends on the Database."""

    def __init__(self, db: Database):
        self.db = db

    def fetch_data(self) -> list[str]:
        return self.db.get_data()


# 1. Create a container instance.
container = Container()

# 2. Register the DataService with a 'REQUEST' scope.
# This means a new instance will be created every time it's resolved.
# The Database dependency is not registered, so the container will create it automatically.
container.register(DataService, scope=Scope.REQUEST)

# 3. Resolve the dependency.
# The container will instantiate DataService and its dependency, Database.
service = container.resolve(DataService)

print(f"Data fetched: {service.fetch_data()}")

# 4. Resolving the same service again will create a new instance due to the REQUEST scope.
service2 = container.resolve(DataService)
assert service is not service2

print("\nBasic usage example updated successfully.")
