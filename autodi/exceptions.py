class DependencyError(Exception):
    """Base dependency injection error."""


class DependencyResolutionError(DependencyError):
    """Failed to resolve a dependency."""


class AsyncDependencyError(DependencyError):
    """Async dependency error."""


class CircularDependencyError(DependencyError):
    """Circular dependency detected."""
