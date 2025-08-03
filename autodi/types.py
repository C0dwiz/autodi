from typing import TypeVar, Type, Callable, Generic
from dataclasses import dataclass

T = TypeVar("T")


@dataclass(frozen=True)
class DependencyConfig(Generic[T]):
    implementation: Type[T] | Callable[..., T]
    is_singleton: bool = False


InjectionTarget = Type[T] | Callable[..., T]
