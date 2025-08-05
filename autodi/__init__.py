from .config.config import DIConfig
from .container import Container, inject
from .exceptions import (
    AsyncDependencyError,
    CircularDependencyError,
    DependencyError,
    DependencyResolutionError,
    ProviderError,
    ScopeError,
)
from .scopes import Scope
from .utils.plugins import ContainerWithPlugins, DIPlugin

__all__ = [
    "Container",
    "inject",
    "DependencyError",
    "DependencyResolutionError",
    "AsyncDependencyError",
    "CircularDependencyError",
    "ScopeError",
    "ProviderError",
    "DIConfig",
    "ContainerWithPlugins",
    "DIPlugin",
    "Scope",
]

__version__ = (1, 0, 2)