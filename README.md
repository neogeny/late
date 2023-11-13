[
    ![lincense](https://img.shields.io/github/license/neogeny/Late)
](https://www.gnu.org/licenses/lgpl-3.0.html)
[
    ![version](https://img.shields.io/pypi/pyversions/late.svg)
](https://www.python.org/downloads/)
[
    ![fury](https://badge.fury.io/py/Late.svg)
](https://pypi.org/project/Late/)
![downloada](https://img.shields.io/pypi/dm/Late.svg)
[
    ![tests](https://github.com/neogeny/late/actions/workflows/default.yml/badge.svg)
](https://github.com/neogeny/late/actions/workflows/default.yml)

# Late
Late binding for Python default arguments


## What is it?

**Late** provides decorators and functions to work around the issues that early binding of
default argument values produces in Python.

What follows is not intuitive for newcomers to Python, but it's something that everyone learns quickly:

```python
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

```python
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

Another problem with the above declaration is that calling ``f(None)`` passes type checking, 
when that's probably not the preferred situation.


## A solution

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


### Working with classes

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


### Working with iterators

**Late** allows passing an iterator as a default argument value, 
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

This is a possible use for the iterator feature. Imagine a function that requires a unique ID, and 
will generate one if none is provided. Without **Late** the declaration would be:

```python
def get_session(uniqueid: int | None = None) -> Session:
    if uniqueid is None:
        uniqueid = make_unique_id()
```

Using **Late**, the declaration can be:

```python
def unique_id_generator() -> Iterator[int]:
    while True:
        yield make_unique_id()
        
def get_session(uniqueid: int = __(unique_id_generator())) -> Session:
```


### Working with functions

**Late** also allows late-binding for functions, so the above example could be implemented using 
a function instead of a generator:

```python
def get_session(uniqueid: int = __(make_unique_id)) -> Session:
```

The given function will be called once every time the ``uniqueid`` parameter is omitted.

### About name choice

The names of what **Late** exports are chosen to be explicit where it matters, and to not get in
the way of the visuals of a declaration. In particular, ``__()`` was chosen to interfere the least 
possible with reading a function declaration (``late()`` is another name for it, and ``__`` is 
seldom used in Python code).

At any rate, **Late** is so simple and so small that you can apply any changes you like and use it as another part of your code instead of installing it as a library.


### How does it work?

For values of immutable types, ``__()`` will return the same value. For all other types ``__()`` 
will wrap the value in a special ``namedtuple(actual=value)``. At function invocation time, this it what happens:

* if the argument name is already in ``kwargs``, nothing is done
* if the wrapped value is an iterator, then ``next(actual)`` is used
* if the wrapped value is a function, then ``actual()`` is used
* in all other cases ``copy.deepcopy(actual)`` is used

For convenient type checking, ``__()`` is declared so its type will be the desired one depending
on the argument:

```python
def late(o: _T | Iterator[_V] | Callable[[], _R]) -> _T | _V | _R:
```

### Why doesn't the Python interpreter solve this?

Although the ugliness and inconvenience in the current situation has ben acknowledged 
and discussed for a very long time, there has never been an agreement about the usefulness,
the semantics, nor the syntax for a solution. That way the _status quo_ has remained unchanged.

You can find a recent discussion about these topics on the 
[Python Ideas](https://discuss.python.org/t/revisit-mutable-default-arguments/)  
site.

## Installation

```bash
$ pip install Late
```

## License

**Late** is licensed as reads in 
[LICENSE](https://github.com/neogeny/late/blob/master/LICENSE).
