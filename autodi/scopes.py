from typing import Literal, NewType

ScopeType = Literal["app", "request"]


class Scope:
    """Defines standard names for dependency scopes."""

    APP: ScopeType = "app"
    "Scope for dependencies that live for the entire application lifecycle (singletons)."

    REQUEST: ScopeType = "request"
    "Scope for dependencies that are created for each request and destroyed afterward."


# Example NewType definitions for creating distinct dependency aliases.
RedisPool = NewType("RedisPool", object)
"A NewType for a Redis connection pool."

DbSession = NewType("DbSession", object)
"A NewType for a database session."
