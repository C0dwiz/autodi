from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar, Union

from .scopes import ScopeType

T = TypeVar("T")


class DependencyKey(Generic[T]):
    """A key to identify a dependency, considering its scope."""

    __slots__ = ("interface", "scope")

    def __init__(self, interface: Any, scope: ScopeType):
        """Initializes the DependencyKey.

        Args:
            interface: The type or NewType of the dependency.
            scope: The scope of the dependency.
        """
        self.interface = interface
        self.scope = scope

    def __hash__(self) -> int:
        """Computes the hash for the key."""
        return hash((self.interface, self.scope))

    def __eq__(self, other: object) -> bool:
        """Checks for equality with another DependencyKey."""
        if not isinstance(other, DependencyKey):
            return NotImplemented
        return self.interface == other.interface and self.scope == other.scope

    def __repr__(self) -> str:
        """Returns a string representation of the key."""
        return f"DependencyKey({self.interface.__name__}, {self.scope})"


class DependencyConfig(Generic[T]):
    """Configuration for a registered dependency."""

    __slots__ = ("implementation", "scope", "init_hook", "destroy_hook")

    def __init__(
        self,
        implementation: Any,
        scope: ScopeType = "app",
        init_hook: str | None = None,
        destroy_hook: str | None = None,
    ):
        """Initializes the DependencyConfig.

        Args:
            implementation: The class or function to instantiate.
            scope: The scope of the dependency.
            init_hook: The name of the method to call after creation.
            destroy_hook: The name of the method to call on scope cleanup.
        """
        self.implementation = implementation
        self.scope = scope
        self.init_hook = init_hook
        self.destroy_hook = destroy_hook


InjectionTarget = Union[type[T], Callable[..., T]]
"A type hint for a dependency that can be a class or a factory function."
