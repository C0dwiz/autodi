from __future__ import annotations

import asyncio
from typing import NewType

from fastapi import Depends, FastAPI

from autodi import Container, Scope
from autodi.extensions.fastapi import setup_dependency_injection

# --- Define Dependencies ---

class Database:
    """A dummy database class with an async lifecycle."""
    def __init__(self, db_url: str):
        """Initializes the Database.

        Args:
            db_url: The URL of the database to connect to.
        """
        self._url = db_url
        self._is_connected = False

    async def connect(self):
        """Simulates an asynchronous connection to the database."""
        print(f"DB: Connecting to {self._url}...")
        await asyncio.sleep(0.01)
        self._is_connected = True

    async def close(self):
        """Simulates an asynchronous disconnection from the database."""
        print(f"DB: Closing connection to {self._url}...")
        await asyncio.sleep(0.01)
        self._is_connected = False

    def query(self, sql: str) -> list[str]:
        """Simulates querying the database.

        Args:
            sql: The SQL query to execute.

        Returns:
            A list of dummy rows.
        """
        if not self._is_connected:
            raise RuntimeError("Database not connected")
        return [f"row from {self._url}"]

# Use NewType to define distinct database dependencies
PrimaryDatabase = NewType("PrimaryDatabase", Database)
ReplicaDatabase = NewType("ReplicaDatabase", Database)

# --- Configure Container ---

container = Container()

# Register the primary database with its lifecycle hooks
container.register(
    PrimaryDatabase,
    provider=lambda: Database("postgresql://primary"),
    scope=Scope.REQUEST,
    init_hook="connect",
    destroy_hook="close",
)

# Register the replica database
container.register(
    ReplicaDatabase,
    provider=lambda: Database("postgresql://replica"),
    scope=Scope.REQUEST,
    init_hook="connect",
    destroy_hook="close",
)

# --- Setup FastAPI ---

app = FastAPI(title="autodi FastAPI Example")

# This middleware will manage the REQUEST scope for each incoming request
setup_dependency_injection(app, container)


# --- Define Endpoints ---

def resolve(dep_type):
    """A helper to create a FastAPI dependency from a container resolution."""
    return Depends(lambda: container.resolve_async(dep_type))


@app.get("/users")
async def get_users(db: PrimaryDatabase = resolve(PrimaryDatabase)):
    """This endpoint reads from the primary database."""
    users = db.query("SELECT * FROM users")
    return {"source": "primary", "users": users}


@app.get("/reports")
async def get_reports(db: ReplicaDatabase = resolve(ReplicaDatabase)):
    """This endpoint reads from the replica database."""
    reports = db.query("SELECT * FROM reports")
    return {"source": "replica", "reports": reports}


# To run: uvicorn examples.fastapi_example:app --reload