import asyncio
from autodi import Container, Scope


class DatabaseConnection:
    """A dummy class that simulates a resource with a connect/disconnect cycle."""

    def __init__(self, db_name: str):
        """Initializes the DatabaseConnection.

        Args:
            db_name: The name of the database.
        """
        self._db_name = db_name
        self._is_connected = False

    async def connect(self):
        """Simulates an asynchronous connection to the database."""
        print(f"DB: Connecting to {self._db_name}...")
        await asyncio.sleep(0.01)  # Simulate async I/O
        self._is_connected = True
        print("DB: Connected.")

    async def close(self):
        """Simulates an asynchronous disconnection from the database."""
        print("DB: Closing connection...")
        await asyncio.sleep(0.01)
        self._is_connected = False
        print("DB: Closed.")

    def query(self, sql: str) -> str:
        """Simulates querying the database.

        Args:
            sql: The SQL query to execute.

        Returns:
            A dummy result string.
        """
        if not self._is_connected:
            raise RuntimeError("Database is not connected")
        return f'Result for "{sql}'"


async def main():
    """Main function to demonstrate lifecycle hooks."""
    # 1. Create a container.
    container = Container()

    # 2. Register the DatabaseConnection.
    # We define a provider to pass arguments to its constructor.
    # We specify `init_hook` and `destroy_hook` to manage its lifecycle.
    container.register(
        DatabaseConnection,
        provider=lambda: DatabaseConnection("my_db"),
        scope=Scope.REQUEST,
        init_hook="connect",
        destroy_hook="close",
    )

    # 3. Enter an async scope, which simulates a web request or a worker task.
    print("--- Entering REQUEST scope ---")
    async with container.enter_scope_async(Scope.REQUEST):
        # 4. Resolve the dependency.
        # The container will call the provider, then `await .connect()` automatically.
        db_conn = await container.resolve_async(DatabaseConnection)

        # 5. Use the dependency.
        print(f"DB Query: {db_conn.query('SELECT * FROM users')}")

    # 6. When the scope exits, the container automatically calls `await .close()`.
    print("--- Exited REQUEST scope ---")


if __name__ == "__main__":
    asyncio.run(main())