import inspect
from collections import defaultdict
from collections.abc import AsyncGenerator, Callable, Generator
from contextlib import asynccontextmanager, contextmanager
from typing import Any, TypeVar

from .exceptions import (
    CircularDependencyError,
    DependencyResolutionError,
    ProviderError,
    ScopeError,
)
from .scopes import Scope, ScopeType
from .types import InjectionTarget

T = TypeVar("T")


class Provider:
    """A provider for creating dependency instances."""

    __slots__ = ("factory", "scope", "init_hook", "destroy_hook")

    def __init__(
        self,
        factory: Callable[..., Any],
        scope: ScopeType,
        init_hook: str | None = None,
        destroy_hook: str | None = None,
    ) -> None:
        """Initializes a Provider.

        Args:
            factory: The function that creates the dependency instance.
            scope: The scope in which the dependency should live.
            init_hook: The name of the method to call after creation.
            destroy_hook: The name of the method to call on scope cleanup.
        """
        self.factory = factory
        self.scope = scope
        self.init_hook = init_hook
        self.destroy_hook = destroy_hook

    async def __call__(self) -> Any:
        """Creates and initializes the dependency instance.

        Returns:
            The created and initialized dependency instance.
        """
        instance = self.factory()
        if inspect.isawaitable(instance):
            instance = await instance

        if self.init_hook and hasattr(instance, self.init_hook):
            hook = getattr(instance, self.init_hook)
            result = hook()
            if inspect.isawaitable(result):
                await result
        return instance


class Container:
    """A dependency injection container with support for scopes and lifecycle hooks."""

    def __init__(self) -> None:
        """Initializes the Container."""
        self._providers: dict[Any, Provider] = {}
        self._scoped_instances: defaultdict[ScopeType, dict[Any, Any]] = defaultdict(dict)
        self._resolution_stack: list[Any] = []
        self._current_scope: ScopeType | None = None

    def register(
        self,
        interface: Any,
        implementation: InjectionTarget[Any] | None = None,
        *,
        scope: ScopeType = Scope.APP,
        provider: Callable[..., Any] | None = None,
        init_hook: str | None = None,
        destroy_hook: str | None = None,
    ) -> None:
        """Registers a dependency with the container.

        Args:
            interface: The type or NewType to register.
            implementation: The class or function to instantiate.
            scope: The scope of the dependency (e.g., APP, REQUEST).
            provider: A factory function to create the instance.
            init_hook: The name of a method to call after instantiation.
            destroy_hook: The name of a method to call when the scope is cleaned up.
        """
        if implementation and provider:
            raise ValueError("Cannot specify both 'implementation' and 'provider' simultaneously.")

        impl = implementation or interface

        def factory() -> Any:
            if isinstance(impl, type):
                return self._instantiate_class(impl)
            if callable(impl):
                return impl()
            return impl

        self._providers[interface] = Provider(provider or factory, scope, init_hook, destroy_hook)

    def override_provider(
        self,
        interface: Any,
        provider: Callable[..., Any],
        scope: ScopeType = Scope.REQUEST,
    ) -> None:
        """Overrides an existing provider, useful for testing.

        Args:
            interface: The type or NewType to override.
            provider: The new factory function.
            scope: The scope of the new provider.
        """
        self._providers[interface] = Provider(provider, scope)

    def resolve(self, target: Any) -> Any:
        """Synchronously resolves a dependency.

        Args:
            target: The type or NewType of the dependency to resolve.

        Returns:
            The resolved dependency instance.
        """
        if self._current_scope and target in self._scoped_instances[self._current_scope]:
            return self._scoped_instances[self._current_scope][target]

        if target in self._scoped_instances[Scope.APP]:
            return self._scoped_instances[Scope.APP][target]

        provider = self._get_provider(target)
        self._check_scope(target, provider)

        if target in self._resolution_stack:
            raise CircularDependencyError(self._resolution_stack + [target])

        self._resolution_stack.append(target)
        try:
            instance = provider.factory()
            if provider.scope:
                self._scoped_instances[provider.scope][target] = instance  # type: ignore
            return instance
        except Exception as e:
            raise ProviderError(target, str(e)) from e
        finally:
            self._resolution_stack.pop()

    async def resolve_async(self, target: Any) -> Any:
        """Asynchronously resolves a dependency.

        Args:
            target: The type or NewType of the dependency to resolve.

        Returns:
            The resolved dependency instance.
        """
        if self._current_scope and target in self._scoped_instances[self._current_scope]:
            return self._scoped_instances[self._current_scope][target]

        if target in self._scoped_instances[Scope.APP]:
            return self._scoped_instances[Scope.APP][target]

        provider = self._get_provider(target)
        self._check_scope(target, provider)

        if target in self._resolution_stack:
            raise CircularDependencyError(self._resolution_stack + [target])

        self._resolution_stack.append(target)
        try:
            instance = await provider()
            if provider.scope:
                self._scoped_instances[provider.scope][target] = instance  # type: ignore
            return instance
        except Exception as e:
            raise ProviderError(target, str(e)) from e
        finally:
            self._resolution_stack.pop()

    def _get_provider(self, target: Any) -> Provider:
        """Retrieves or creates a provider for a given target.

        Args:
            target: The type or NewType to find a provider for.

        Returns:
            The found or created Provider instance.
        """
        provider = self._providers.get(target)
        if not provider:
            if isinstance(target, type):
                return Provider(lambda: self._instantiate_class(target), Scope.REQUEST)
            raise DependencyResolutionError(target, "No provider registered")
        return provider

    def _check_scope(self, target: Any, provider: Provider) -> None:
        """Checks if a dependency can be resolved in the current scope.

        Args:
            target: The dependency being resolved.
            provider: The provider for the dependency.

        Raises:
            ScopeError: If the dependency's scope is not compatible with the current scope.
        """
        if provider.scope != self._current_scope and self._current_scope is not None:
            if provider.scope != Scope.APP and self._current_scope != Scope.APP:
                raise ScopeError(
                    str(provider.scope),
                    f"Cannot resolve {target} with scope {provider.scope} "
                    f"in {self._current_scope} scope",
                )

    def _instantiate_class(self, cls: type[T]) -> T:
        """Instantiates a class by resolving its constructor dependencies.

        Args:
            cls: The class to instantiate.

        Returns:
            An instance of the class.
        """
        if not hasattr(cls, "__init__") or not callable(cls.__init__):
            return cls()

        signature = inspect.signature(cls.__init__)
        kwargs = {}
        for name, param in signature.parameters.items():
            if name == "self":
                continue
            param_type = param.annotation
            if param_type is inspect.Parameter.empty:
                raise ValueError(
                    f"Parameter '{name}' in {cls.__name__}.__init__ has no type annotation"
                )
            kwargs[name] = self.resolve(param_type)
        return cls(**kwargs)

    @contextmanager
    def enter_scope(self, scope_name: ScopeType) -> Generator[None, None, None]:
        """A context manager for entering a synchronous scope.

        Args:
            scope_name: The name of the scope to enter.
        """
        if self._current_scope:
            raise ScopeError(str(scope_name), "Nested scopes are not supported")

        self._current_scope = scope_name
        try:
            yield
        finally:
            self._cleanup_scope(scope_name)
            self._current_scope = None

    @asynccontextmanager
    async def enter_scope_async(self, scope_name: ScopeType) -> AsyncGenerator[None, None]:
        """A context manager for entering an asynchronous scope.

        Args:
            scope_name: The name of the scope to enter.
        """
        if self._current_scope:
            raise ScopeError(str(scope_name), "Nested scopes are not supported")

        self._current_scope = scope_name
        try:
            yield
        finally:
            await self._cleanup_scope_async(scope_name)
            self._current_scope = None

    def _cleanup_scope(self, scope_name: ScopeType) -> None:
        """Cleans up a synchronous scope, calling destroy hooks.

        Args:
            scope_name: The name of the scope to clean up.
        """
        if scope_name in self._scoped_instances:
            for interface, instance in self._scoped_instances[scope_name].items():
                provider = self._providers.get(interface)
                if provider and provider.destroy_hook and hasattr(instance, provider.destroy_hook):
                    getattr(instance, provider.destroy_hook)()
            del self._scoped_instances[scope_name]

    async def _cleanup_scope_async(self, scope_name: ScopeType) -> None:
        """Cleans up an asynchronous scope, calling destroy hooks.

        Args:
            scope_name: The name of the scope to clean up.
        """
        if scope_name in self._scoped_instances:
            for interface, instance in self._scoped_instances[scope_name].items():
                provider = self._providers.get(interface)
                if provider and provider.destroy_hook and hasattr(instance, provider.destroy_hook):
                    hook = getattr(instance, provider.destroy_hook)
                    result = hook()
                    if inspect.isawaitable(result):
                        await result
            del self._scoped_instances[scope_name]

    def cleanup(self) -> None:
        """Cleans up the APP scope synchronously."""
        self._cleanup_scope(Scope.APP)

    async def cleanup_async(self) -> None:
        """Cleans up the APP scope asynchronously."""
        await self._cleanup_scope_async(Scope.APP)


def inject(
    container: Container, *, scope: ScopeType = Scope.APP
) -> Callable[[InjectionTarget[T]], InjectionTarget[T]]:
    """A decorator to register a class with the container.

    Args:
        container: The container instance to register with.
        scope: The scope of the dependency.

    Returns:
        A decorator function.
    """

    def decorator(cls: InjectionTarget[T]) -> InjectionTarget[T]:
        if not isinstance(cls, type):
            raise TypeError("@inject decorator can only be applied to classes")
        container.register(cls, scope=scope)
        return cls

    return decorator
