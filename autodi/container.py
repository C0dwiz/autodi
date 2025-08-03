from __future__ import annotations
import sys
from typing import Dict, Optional, TypeVar, Type, Any, Callable, cast, get_type_hints
from .types import DependencyConfig, InjectionTarget
from .exceptions import DependencyResolutionError, CircularDependencyError
import inspect

T = TypeVar("T")


class Container:
    def __init__(self):
        self._dependencies: dict[Type[Any], DependencyConfig[Any]] = {}
        self._singletons: dict[Type[Any], Any] = {}
        self._resolution_stack: set[Type[Any]] = set()
        self._init_hook_name: Optional[str] = None
        self._destroy_hook_name: Optional[str] = None
        self._destroy_callbacks: Dict[Type, Callable[[], None]] = {}

    def register(
        self,
        interface: Type[T],
        implementation: InjectionTarget[T] | None = None,
        *,
        is_singleton: bool = False,
        init_hook: Optional[str] = None,
        destroy_hook: Optional[str] = None,
    ) -> None:
        impl = implementation or interface
        self._dependencies[interface] = DependencyConfig[T](
            implementation=impl, is_singleton=is_singleton
        )

        if destroy_hook:

            def cleanup():
                if instance := self._singletons.get(interface):
                    if hasattr(instance, destroy_hook):
                        getattr(instance, destroy_hook)()

            self._destroy_callbacks[interface] = cleanup

        if init_hook:
            self._init_hook_name = init_hook

    def resolve(self, target: InjectionTarget[T]) -> T:
        target_type = (
            target if isinstance(target, type) else self._get_return_type(target)
        )

        if target_type in self._singletons:
            return cast(T, self._singletons[target_type])

        if target_type in self._resolution_stack:
            raise CircularDependencyError(
                f"Circular dependency detected for {getattr(target_type, '__name__', target_type)}"
            )

        self._resolution_stack.add(target_type)
        try:
            config = self._dependencies.get(target_type)
            impl = config.implementation if config else target

            if isinstance(impl, type):
                instance = self._instantiate_class(impl)
            else:
                instance = impl

            if config and config.is_singleton:
                self._singletons[target_type] = instance

            return cast(T, instance)
        finally:
            self._resolution_stack.discard(target_type)

    def _instantiate_class(self, cls: Type[Any]) -> Any:
        if cls.__init__ is object.__init__:
            instance = cls()
        else:
            frame = sys._getframe(2)
            localns = {**frame.f_locals, **globals()}
            try:
                type_hints = get_type_hints(cls.__init__, localns=localns)
            except NameError:
                type_hints = get_type_hints(cls.__init__, localns=locals())

            dependencies = {}
            for name, dep_type in type_hints.items():
                if name == "return":
                    continue
                try:
                    dependencies[name] = self.resolve(dep_type)
                except Exception as e:
                    raise DependencyResolutionError(
                        f"Failed to resolve {dep_type} for {cls.__name__}: {str(e)}"
                    ) from e

            instance = cls(**dependencies)

        try:
            if hasattr(self, "_init_hook_name") and self._init_hook_name:
                if hasattr(instance, self._init_hook_name):
                    getattr(instance, self._init_hook_name)()
        except Exception as e:
            raise DependencyResolutionError(
                f"Init hook failed for {cls.__name__}: {str(e)}"
            ) from e

        return instance

    def _get_return_type(self, func: Callable[..., Any]) -> Type[Any]:
        hints = get_type_hints(func)
        return cast(Type[Any], hints.get("return", object))

    async def resolve_async(self, target: InjectionTarget[T]) -> T:
        instance = self.resolve(target)

        if inspect.iscoroutinefunction(instance):
            return cast(T, await instance())
        if inspect.isawaitable(instance):
            return cast(T, await instance)
        return cast(T, instance)

    def cleanup(self) -> None:
        for callback in self._destroy_callbacks.values():
            callback()
        self._singletons.clear()

    def clear(self) -> None:
        self._dependencies.clear()
        self._singletons.clear()


def inject(
    container: Container, *, is_singleton: bool = False
) -> Callable[[InjectionTarget[T]], InjectionTarget[T]]:
    def decorator(cls: InjectionTarget[T]) -> InjectionTarget[T]:
        if not isinstance(cls, type):
            raise TypeError("Decorator can only be applied to classes")
        container.register(cast(Type[T], cls), is_singleton=is_singleton)
        return cls

    return decorator
