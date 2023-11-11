# Late
Late binding for Python default arguments


## What is it?

**Late** provides decorators and functions to work around the issues that early binding of
default values produces in Python.

This is not intuitive for newcomers to Python, but it's something that everyone learns quickly:

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

The behavior in Python is that the same ``[]`` initializer is passed on every function
invocation.

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

Now comes the orther ugly part.  When using type annotations, the above function must be declared in away that type checkers do not complain about using ``None`` as the default value:


```python
>>> def f(x: list[Any] | None = None) -> list[Any]:
```


**Late** provides a way to solve the above ugliness with some decorator magic. This is how the new code would look with some magic:

```python
from late import latebinding, __


@latebinding
def f(x: list[Any] = __([])) -> list[Any]:
    x.append(1)
    return x
```


## About name choice

The names of what **Late** exports are chosen to be explicit where it matters, and to not get in
the way of the vissuals of a declaration. In particular, ``__()`` was chose to intefere the least possible with reading a function declaration (``late()`` is another name for it).

At any rate, **Late** is so simple and so small that you can apply any changes you like and use it as another part of your code instead of installing it as a library.


## License

**Late** is under the  _GNU GENERAL PUBLIC LICENSE Version 3_, as reades in the
[LICENSE)(LICENSE) file.
