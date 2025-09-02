from __future__ import annotations

import inspect
from enum import Enum
from typing import Any, Callable

PRIMITIVE_TYPES = (int, float, str, bool, bytes, type(None))
COLLECTION_TYPES = (list, tuple, dict, set, frozenset)
BUILTIN_TYPES = PRIMITIVE_TYPES + COLLECTION_TYPES


class Match[V]:
    def __init__(self, value: V) -> None:
        self.value = value

    def case[P, R](
        self,
        pattern: P | type[P],
        then: R | Callable[[P], R] | Callable[[], R],
    ) -> Case[V, P, R]:
        if type(pattern) is type:
            matched = isinstance(self.value, pattern)
        else:
            if type(pattern) in PRIMITIVE_TYPES or isinstance(pattern, Enum):
                # Primitive type matching
                matched = self.value == pattern
            elif type(pattern) in COLLECTION_TYPES:
                # Collection type matching
                matched = False  # TODO: implement collection matching
            else:
                # Custom type matching
                matched = type(pattern) is type(self.value)

        return Case(self.value, then, matched)  # type: ignore


class Case[V, P, R]:
    def __init__(self, value: V, then: R | Callable[[P], R] | Callable[[], R], matched: bool) -> None:
        self.value = value
        self.then = then
        self.matched = matched

    def case[UP, UR](
        self,
        pattern: UP | type[UP],
        then: UR | Callable[[UP], UR] | Callable[[], UR],
    ) -> Case[V, P | UP, R | UR]:
        if self.matched:
            return self  # type: ignore

        if type(pattern) is type:
            matched = isinstance(self.value, pattern)
        else:
            if type(pattern) in PRIMITIVE_TYPES or isinstance(pattern, Enum):
                # Primitive type matching
                matched = self.value == pattern
            elif type(pattern) in COLLECTION_TYPES:
                # Collection type matching
                matched = False  # TODO: implement collection matching
            else:
                # Custom type matching
                matched = type(pattern) is type(self.value)

        return Case(self.value, then, matched)  # type: ignore

    def exhaustive(self, eval: bool = True) -> R:
        if not self.matched:
            raise ExhaustiveError(self.value)
        if eval:
            return _unwrap(self.value, self.then)
        else:
            return self.then  # type: ignore

    def otherwise[UR](self, default: UR | Callable[[], UR], eval: bool = True) -> R | UR:
        if self.matched:
            if eval:
                return _unwrap(self.value, self.then)
            else:
                return self.then  # type: ignore
        if eval and callable(default):
            return default()  # type: ignore
        return default


def match[V](value: V) -> Match[V]:
    return Match[V](value)


def _unwrap[V, R](value: V, then: R | Callable[[V], R] | Callable[[], R]) -> R:
    if not callable(then):
        return then

    # For classes (prevent constructor invocation)
    if inspect.isclass(then):
        return then  # type: ignore
    
    # Only call for functions or methods
    sig = inspect.signature(then)
    if len(sig.parameters) == 0:
        return then()  # type: ignore
    else:
        return then(value)  # type: ignore


class ExhaustiveError(Exception):
    def __init__(self, value: Any) -> None:
        super().__init__(f"Non-exhaustive match. Unhandled value: {value}")
        self.value = value
