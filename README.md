# match-expression

A Python implementation of TypeScript's [ts-pattern](https://github.com/gvergnaud/ts-pattern), bringing powerful, type-safe pattern matching to Python with an expressive, chainable API.

## Features

- **Chainable API**: Intuitive `match(value).case(pattern, then).exhaustive()` syntax
- **Type-safe**: Full type inference support with pyright/mypy
- **Exhaustiveness checking**: Ensures all cases are handled at compile time
- **Zero dependencies**: Lightweight and fast
- **Pythonic**: Leverages Python 3.10+ type system features

## Installation

```bash
pip install match_expression
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
git clone https://github.com/qodot/match-expression.git
cd match-expression
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

## Requirements

- Python 3.10 or higher
- No external dependencies

## License

MIT License - see LICENSE file for details