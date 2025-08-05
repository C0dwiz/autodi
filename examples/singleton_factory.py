from autodi import Container, Scope


class ConfigService:
    """A simple configuration service."""

    def __init__(self):
        self.theme = "dark"
        self.debug = True


def create_connection() -> dict[str, str]:
    """A factory function to create a connection dictionary."""
    print("Factory: Creating connection...")
    return {"status": "connected"}


# 1. Create a container instance.
container = Container()

# 2. Register ConfigService as an APP-scoped dependency (a singleton).
container.register(ConfigService, scope=Scope.APP)

# 3. Register a factory (provider) for a dictionary dependency.
# It is also APP-scoped, so the factory will only be called once.
container.register(dict, provider=create_connection, scope=Scope.APP)

# --- Resolving dependencies ---

print("Resolving ConfigService...")
config1 = container.resolve(ConfigService)
config2 = container.resolve(ConfigService)

# Both resolutions should return the exact same instance.
assert config1 is config2
print(f"Config theme: {config1.theme}")

print("\nResolving connection...")
connection1 = container.resolve(dict)
connection2 = container.resolve(dict)

# The factory `create_connection` should have been called only once.
assert connection1 is connection2
print(f"Connection status: {connection1['status']}")

print("\nSingleton factory example updated successfully.")
