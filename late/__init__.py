import copy
import functools
import inspect
from collections.abc import Callable, Iterator
from typing import Any, NamedTuple, TypeVar

__all__ = ['latebinding']


_R = TypeVar('_R')
_T = TypeVar('_T')
_V = TypeVar('_V')


class _LateBound(NamedTuple):
    actual: Any


def late(o: _T | Iterator[_V] | Callable[[], _R]) -> _T | _V | _R:
    if o is None or isinstance(o, int | float | bool | str | bytes | tuple | frozenset):
        return o  # type: ignore

    return _LateBound(actual=o)  # type: ignore


__ = late
包 = late


def _resolve_value(value):
    if isinstance(value, _LateBound):
        value = value.actual
    if isinstance(value, int | float | str | bytes | bool | tuple | bytearray | frozenset):
        return value
    if isinstance(value, Iterator):
        return next(value)
    if inspect.isfunction(value):
        return value()
    return copy.deepcopy(value)


def _lateargs(func: Callable, **kwargs) -> dict[str, Any]:

    lateargs = {
        name: _resolve_value(param.default)
        for name, param in inspect.signature(func).parameters.items()
        if name not in kwargs and param.default != inspect._empty
    }
    return {**kwargs, **lateargs}


def latebinding(target: Callable | type) -> Callable | type:
    if type(target) is type:
        return _latebindclass(target)

    @functools.wraps(target)
    def wrapper(*args, **kwargs):
        kwargs = _lateargs(target, **kwargs)
        return target(*args, **kwargs)

    return wrapper


def _latebindclass(cls: type) -> type:
    old_init = cls.__init__  # type: ignore[misc]

    @functools.wraps(old_init)
    def new_init(self, *args, **kwargs):
        kwargs = _lateargs(old_init, **kwargs)
        old_init(self, *args, **kwargs)

    cls.__init__ = new_init  # type: ignore[misc]
    return cls
