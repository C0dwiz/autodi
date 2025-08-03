from typing import Type, TypeVar, Any
from abc import ABC, abstractmethod

T = TypeVar("T")


class DIPlugin(ABC):
    @abstractmethod
    def pre_resolve(self, interface: Type[T]) -> None:
        pass

    @abstractmethod
    def post_resolve(self, instance: Any) -> None:
        pass


class ContainerWithPlugins:
    def __init__(self, container):
        self._container = container
        self._plugins: list[DIPlugin] = []

    def add_plugin(self, plugin: DIPlugin) -> None:
        self._plugins.append(plugin)

    def resolve(self, target: Type[T]) -> T:
        for plugin in self._plugins:
            plugin.pre_resolve(target)

        instance = self._container.resolve(target)

        for plugin in self._plugins:
            plugin.post_resolve(instance)

        return instance
