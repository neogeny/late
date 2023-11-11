![lincense](https://img.shields.io/github/license/neogeny/Late)
![version](https://img.shields.io/pypi/pyversions/late.svg)
![fury](https://badge.fury.io/py/Late.svg)
![downloada](https://img.shields.io/pypi/dm/Late.svg)

# Late
Late binding for Python default arguments


## What is it?

**Late** provides decorators and functions to work around the issues that early binding of
default argument values produces in Python.

What follows is not intuitive for newcomers to Python, but it's something that everyone learns quickly:

```python-repl
>>> def f(x=[]):
...     x.append(1)
...     return x
...
>>> f()
[1]
>>> f()
[1, 1]
>>> f()
[1, 1, 1]
```

The behavior in Python is that the same initializer value is passed on every function
invocation, so using mutable values produces the above results.

The coding pattern to work around the above is to use ``None`` as the initializer, and check for
the parameter value at the start of the function code:

```python-repl
>>> def f(x=None):
...     if x is None:
...         x = []
...     x.append(1)
...     return x
...
>>> f()
[1]
>>> f()
[1]
>>> f()
[1]
```

It's ugly, but it works.

Now comes the other ugly part.  When using type annotations, the above function must be declared 
in a way so that type checkers do not complain about using ``None`` as the default value:


```python
>>> def f(x: list[Any] | None = None) -> list[Any]:
```


**Late** provides a way to solve the above ugliness with some decorator magic. This is how the code 
looks with some of that magic:

```python
from late import latebinding, __


@latebinding
def f(x: list[Any] = __([])) -> list[Any]:
    x.append(1)
    return x

assert f() == [1]
assert f() == [1]
assert f() == [1]

```


## Working with classes

**Late** also works with classes and `dataclass`. The ``@latebinding`` decorator 
must be the outer one:

```python
@latebinding
@dataclass
class C:
    x: list[Any] = __([])  # noqa

c = C()
assert c.x == []

d = C()
assert d.x == []
c.x = [1]
assert c.x == [1]
assert d.x == []

assert d.x is not c.x

```


## Working with generators

**Late** allows passing a generator as a default argument value, 
and it will provide the next value on each function call. The usefulness of
this feature is unknown, but it's something that came up during the discussions
about default arguments, so **Late** implements it.


```python
    def fib() -> Iterator[int]:
        x, y = 0, 1
        while True:
            yield x
            x, y = y, x + y


    @latebinding
    def f(x: int = __(fib())) -> int:
        return x

    assert f() == 0
    assert f() == 1
    assert f() == 1
    assert f() == 2
    assert f() == 3
    assert f() == 5
```


## About name choice

The names of what **Late** exports are chosen to be explicit where it matters, and to not get in
the way of the visuals of a declaration. In particular, ``__()`` was chosen to interfere the least 
possible with reading a function declaration (``late()`` is another name for it, and ``__`` is 
seldom used in Python code).

At any rate, **Late** is so simple and so small that you can apply any changes you like and use it as another part of your code instead of installing it as a library.


## Installation

```bash
$ pip install Late
```

## License

**Late** is licensed under the  _GNU LESSER GENERAL PUBLIC LICENSE Version 3_, as reads in the
[LICENSE](LICENSE) file.
