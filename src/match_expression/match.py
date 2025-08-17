from __future__ import annotations

import inspect
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
            result = _unwrap(self.value, then)
        else:
            if type(pattern) in PRIMITIVE_TYPES:
                # 원시 타입 매칭
                matched = self.value == pattern
                result = _unwrap(self.value, then)
            elif type(pattern) in COLLECTION_TYPES:
                # 컬렉션 타입 매칭
                result = _unwrap(self.value, then)
            else:
                # 커스텀 타입 매칭
                matched = type(pattern) is type(self.value)
                result = _unwrap(self.value, then)

        return Case(self.value, result, matched)  # type: ignore


class Case[V, P, R]:
    def __init__(self, value: V, result: R, matched: bool) -> None:
        self.value = value
        self.result = result
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
            result = _unwrap(self.value, then)
        else:
            if type(pattern) in PRIMITIVE_TYPES:
                # 원시 타입 매칭
                matched = self.value == pattern
                result = _unwrap(self.value, then)
            elif type(pattern) in COLLECTION_TYPES:
                # 컬렉션 타입 매칭
                result = _unwrap(self.value, then)
            else:
                # 커스텀 타입 매칭
                matched = type(pattern) is type(self.value)
                result = _unwrap(self.value, then)

        return Case(self.value, result, matched)  # type: ignore

    def exhaustive(self) -> R:
        if not self.matched:
            raise ExhaustiveError(self.value)
        return self.result

    def otherwise[UR](self, default: UR | Callable[[], UR]) -> R | UR:
        if self.matched:
            return self.result
        if callable(default):
            return default()  # type: ignore
        return default


def match[V](value: V) -> Match[V]:
    return Match[V](value)


def _unwrap[V, R](value: V, then: R | Callable[[V], R] | Callable[[], R]) -> R:
    if not callable(then):
        return then

    sig = inspect.signature(then)
    if len(sig.parameters) == 0:
        return then()  # type: ignore
    else:
        return then(value)  # type: ignore


class ExhaustiveError(Exception):
    def __init__(self, value: Any) -> None:
        super().__init__(f"Non-exhaustive match. Unhandled value: {value}")
        self.value = value
