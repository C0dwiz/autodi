from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable


T = TypeVar("T")


@runtime_checkable
class ResolvableContainer(Protocol):
    """A protocol defining the interface for a container that can resolve dependencies."""

    def resolve(self, target: Any) -> Any:
        """Resolves a dependency.

        Args:
            target: The dependency to resolve.

        Returns:
            The resolved instance.
        """
        ...


class DIPlugin:
    """Base class for DI plugins."""

    def pre_resolve(self, interface: Any) -> None:
        """Called before a dependency is resolved.

        Args:
            interface: The dependency being resolved.
        """

    def post_resolve(self, instance: Any) -> None:
        """Called after a dependency is resolved.

        Args:
            instance: The resolved instance.
        """


class ContainerWithPlugins:
    """A wrapper for a container that allows adding plugins.

    Plugins can execute actions before and after dependency resolution.
    """

    def __init__(self, container: ResolvableContainer):
        """Initializes the ContainerWithPlugins.

        Args:
            container: The container to wrap.
        """
        self._container = container
        self._plugins: list[DIPlugin] = []

    def add_plugin(self, plugin: DIPlugin) -> None:
        """Adds a new plugin to the container.

        Args:
            plugin: The plugin to add.
        """
        self._plugins.append(plugin)

    def resolve(self, target: Any) -> Any:
        """Resolves a dependency, invoking plugin hooks.

        Args:
            target: The dependency to resolve.

        Returns:
            The resolved instance.
        """
        for plugin in self._plugins:
            plugin.pre_resolve(target)

        instance = self._container.resolve(target)

        for plugin in self._plugins:
            plugin.post_resolve(instance)

        return instance


class LoggingPlugin(DIPlugin):
    """An example plugin for logging the dependency resolution process."""

    def pre_resolve(self, interface: Any) -> None:
        """Logs before resolution."""
        print(f"Resolving {interface.__name__}...")

    def post_resolve(self, instance: Any) -> None:
        """Logs after resolution."""
        print(f"Resolved {instance.__class__.__name__} instance.")
