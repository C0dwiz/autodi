from __future__ import annotations


class DependencyError(Exception):
    """Base class for all dependency injection related errors."""

    def __init__(self, message: str = "Dependency injection error occurred"):
        """Initializes the DependencyError.

        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(self.message)


class DependencyResolutionError(DependencyError):
    """Raised when a dependency cannot be resolved."""

    def __init__(self, dependency: type, message: str = "Failed to resolve dependency"):
        """Initializes the DependencyResolutionError.

        Args:
            dependency: The dependency that could not be resolved.
            message: The error message.
        """
        self.dependency = dependency
        full_message = f"{message}: {dependency.__name__}"
        super().__init__(full_message)


class AsyncDependencyError(DependencyError):
    """Raised for errors related to asynchronous dependencies."""


class CircularDependencyError(DependencyError):
    """Raised when a circular dependency is detected."""

    def __init__(
        self, chain: list[type], message: str = "Circular dependency detected"
    ):
        """Initializes the CircularDependencyError.

        Args:
            chain: The chain of dependencies that form the cycle.
            message: The error message.
        """
        self.chain = chain
        chain_names = " -> ".join(t.__name__ for t in chain)
        full_message = f"{message}: {chain_names}"
        super().__init__(full_message)


class ScopeError(DependencyError):
    """Raised for errors related to dependency scopes."""

    def __init__(self, scope: str, message: str = "Scope error"):
        """Initializes the ScopeError.

        Args:
            scope: The scope that caused the error.
            message: The error message.
        """
        self.scope = scope
        full_message = f"{message} (scope: {scope})"
        super().__init__(full_message)


class ProviderError(DependencyError):
    """Raised when a provider fails to create an instance."""

    def __init__(self, provider: type, message: str = "Provider failed"):
        """Initializes the ProviderError.

        Args:
            provider: The provider that failed.
            message: The error message.
        """
        self.provider = provider
        full_message = f"{message} for provider: {provider.__name__}"
        super().__init__(full_message)
