from __future__ import annotations
from typing import Generic, TypeVar, Callable, Any

V = TypeVar("V")  # type of match(value)
P = TypeVar("P")  # type of when(pattern)
UP = TypeVar("UP")  # unionized pattern type of when(pattern)
R = TypeVar("R")  # return type of when(then)
UR = TypeVar("UR")  # unionized return type of when(then)


class Match(Generic[V]):
    def __init__(self, value: V) -> None:
        self.value = value

    def when(
        self,
        pattern: P,
        then: R,
    ) -> When[V, P, R]:
        if isinstance(pattern, type):
            # 타입 매칭
            matched = isinstance(self.value, pattern)
        else:
            # 값 매칭 (리터럴)
            matched = self.value == pattern

        return When(self.value, then, matched)


class When(Generic[V, P, R]):
    def __init__(self, value: V, result: R, matched: bool) -> None:
        self.value = value
        self.result = result
        self.matched = matched

    def when(
        self,
        pattern: UP,
        then: UR,
    ) -> When[V, P | UP, R | UR]:
        if self.matched:
            return self  # type: ignore

        # 타입 매칭 (isinstance)
        if isinstance(pattern, type):
            matched = isinstance(self.value, pattern)
        # 값 매칭 (리터럴 포함)
        else:
            matched = self.value == pattern

        return When(self.value, then, matched)

    def exhaustive(self) -> R:
        if not self.matched:
            raise ExhaustiveError(self.value)
        return self.result

    def otherwise(self, default: UR) -> R | UR:
        if self.matched:
            return self.result
        return default


def match(value: V) -> Match[V]:
    return Match[V](value)


class ExhaustiveError(Exception):
    def __init__(self, value: Any) -> None:
        super().__init__(f"Non-exhaustive match. Unhandled value: {value}")
        self.value = value
