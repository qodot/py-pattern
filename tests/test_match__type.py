from dataclasses import dataclass
from typing import assert_type
import pytest

from match_expression import match, ExhaustiveError


@dataclass
class Animal:
    name: str


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} barks!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} meows!"


class Bird(Animal):
    def speak(self) -> str:
        return f"{self.name} chirps!"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Dog("Buddy"), "Buddy barks!"),
        (Cat("Whiskers"), "Whiskers meows!"),
        (Bird("Tweety"), "Tweety chirps!"),
    ],
)
def test__valid_type(value: Animal, expected: str) -> None:
    result = (
        match(value)
        .case(Dog, lambda dog: dog.speak())
        .case(Cat, lambda cat: cat.speak())
        .case(Bird, lambda bird: bird.speak())
        .exhaustive()
    )

    assert_type(result, str)
    assert result == expected


def test__exhaustive__raises_error() -> None:
    cat = Cat("Whiskers")

    with pytest.raises(ExhaustiveError) as exc_info:
        match(cat).case(Dog, lambda dog: dog.speak()).case(
            Bird, lambda bird: bird.speak()
        ).exhaustive()

    assert isinstance(exc_info.value.value, Cat)


def test__otherwise():
    cat = Cat("Whiskers")

    result = (
        match(cat)
        .case(Dog, lambda dog: dog.speak())
        .case(Bird, lambda bird: bird.speak())
        .otherwise("Other")
    )

    assert_type(result, str)
    assert result == "Other"
