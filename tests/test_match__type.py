import pytest

from py_pattern import match, ExhaustiveError


class Animal:
    pass


class Dog(Animal):
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} barks!"


class Cat(Animal):
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} meows!"


class Bird(Animal):
    def __init__(self, name: str):
        self.name = name

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
        .case(Dog, "Buddy barks!")
        .case(Cat, "Whiskers meows!")
        .case(Bird, "Tweety chirps!")
        .exhaustive()
    )

    assert result == expected


def test__exhaustive__raises_error() -> None:
    cat = Cat("Whiskers")

    with pytest.raises(ExhaustiveError) as exc_info:
        match(cat).case(Dog, "Dog: Buddy").case(Bird, "Bird: Tweety").exhaustive()

    assert isinstance(exc_info.value.value, Cat)


def test__otherwise():
    cat = Cat("Whiskers")

    result = (
        match(cat).case(Dog, "Dog: Buddy").case(Bird, "Bird: Tweety").otherwise("Other")
    )

    assert result == "Other"
