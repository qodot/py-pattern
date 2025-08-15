# py-pattern

A Python implementation of TypeScript's [ts-pattern](https://github.com/gvergnaud/ts-pattern), bringing powerful, type-safe pattern matching to Python with an expressive, chainable API.

## Features

- **Chainable API**: Intuitive `match(value).case(pattern, then).exhaustive()` syntax
- **Type-safe**: Full type inference support with pyright/mypy
- **Exhaustiveness checking**: Ensures all cases are handled at compile time
- **Zero dependencies**: Lightweight and fast
- **Pythonic**: Leverages Python 3.10+ type system features

## Installation

```bash
pip install py-pattern
```

## Quick Start

```python
from typing import Literal
from py_pattern import match

# Literal type matching
def process_status(status: Literal["pending", "success", "error"]) -> int:
    return (
        match(status)
        .case("pending", 0)
        .case("success", 1)
        .case("error", -1)
        .exhaustive()
    )

# Type matching with classes
class Dog:
    def bark(self) -> str:
        return "Woof!"

class Cat:
    def meow(self) -> str:
        return "Meow!"

def handle_animal(animal: Dog | Cat) -> str:
    return (
        match(animal)
        .case(Dog, lambda d: d.bark())
        .case(Cat, lambda c: c.meow())
        .exhaustive()
    )
```

## Examples

### Literal Type Matching

```python
from typing import Literal
from py_pattern import match

type Platform = Literal["web", "mobile", "desktop"]

def get_app_name(platform: Platform) -> str:
    return (
        match(platform)
        .case("web", "Web Application")
        .case("mobile", "Mobile App")
        .case("desktop", "Desktop Software")
        .exhaustive()
    )

# Type checker knows all cases are covered!
```

### Class Type Matching

```python
from py_pattern import match

class Success:
    def __init__(self, value: str):
        self.value = value

class Error:
    def __init__(self, message: str):
        self.message = message

def handle_result(result: Success | Error) -> str:
    return (
        match(result)
        .case(Success, lambda s: f"Success: {s.value}")
        .case(Error, lambda e: f"Error: {e.message}")
        .exhaustive()
    )
```

### Using `otherwise` for Default Cases

```python
from py_pattern import match

def classify_number(n: int) -> str:
    return (
        match(n)
        .case(0, "zero")
        .case(1, "one")
        .case(2, "two")
        .otherwise("many")
    )
```

### Mixed Return Types

The library correctly infers union return types:

```python
from py_pattern import match

def process(value: int | str) -> int | str:
    return (
        match(value)
        .case(int, lambda i: i * 2)      # Returns int
        .case(str, lambda s: s.upper())  # Returns str
        .exhaustive()
    )
    # Type is inferred as: int | str
```

## How It Works

### Type System Design

The library uses Python's powerful type system with TypeVars to ensure type safety:

- **`V`**: The type of the matched value
- **`P`**: The narrowed type after pattern matching
- **`R`**: The return type of the first branch
- **`UR`**: Union of return types from multiple branches

This design enables:
1. **Type narrowing**: In each `when` branch, the value is narrowed to the specific matched type
2. **Return type union**: Different branches can return different types, and the final type is their union
3. **Exhaustiveness checking**: The type system ensures all possible cases are handled

### Example Type Flow

```python
match(value: Dog | Cat | Bird)    # V = Dog | Cat | Bird
  .case(Dog, lambda d: 123)       # P = Dog, R = int
  .case(Cat, lambda c: "hello")   # P = Cat, UR = str
  .case(Bird, lambda b: True)     # P = Bird, UR = bool
  .exhaustive()                   # Returns: int | str | bool
```

## API Reference

### `match(value: V) -> Match[V]`
Starts a pattern matching chain.

### `.case(pattern: P, then: R) -> Case[V, P, R]`
Matches against a pattern. If the pattern matches, executes `then`.

- `pattern`: A value to match against (for literals) or a type (for isinstance checks)
- `then`: The value to return or a function to execute with the matched value

### `.exhaustive() -> R`
Ensures all cases are handled. Raises `ExhaustiveError` if not all cases are covered.

### `.otherwise(default: R) -> R`
Provides a default value for unmatched cases.

## Type Checking

The library is designed to work with type checkers like pyright and mypy:

```bash
# Install pyright
pip install pyright

# Type check your code
pyright your_file.py
```

## Contributing

Contributions are welcome! Here's how to get started:

1. Clone the repository
```bash
git clone https://github.com/qodot/py-pattern.git
cd py-pattern
```

2. Install development dependencies
```bash
uv sync --dev
```

3. Run tests
```bash
uv run pytest
```

4. Type check
```bash
uv run pyright src/ tests/
```

## Comparison with Alternatives

| Feature | py-pattern | Python match/case | Traditional if/elif |
|---------|-----------------|-------------------|-------------------|
| Expression-based | ✅ | ❌ | ❌ |
| Type inference | ✅ | Partial | ❌ |
| Exhaustiveness check | ✅ | ❌ | ❌ |
| Chainable API | ✅ | ❌ | ❌ |
| Runtime overhead | Minimal | None | None |

## Requirements

- Python 3.10 or higher
- No external dependencies

## License

MIT License - see LICENSE file for details

## Acknowledgments

This library is inspired by the excellent [ts-pattern](https://github.com/gvergnaud/ts-pattern) library for TypeScript. We aim to bring the same level of type safety and expressiveness to Python.

## Resources

- [TypeScript ts-pattern](https://github.com/gvergnaud/ts-pattern) - The original inspiration
- [PEP 622](https://www.python.org/dev/peps/pep-0622/) - Structural Pattern Matching in Python
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Python typing module documentation

---

Made with ❤️ for the Python community