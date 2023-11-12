import copy
import functools
import inspect
from collections.abc import Callable, Iterator
from typing import Any, NamedTuple, TypeVar

__all__ = ['latebinding', 'late', '__']


_R = TypeVar('_R')
_T = TypeVar('_T')
_V = TypeVar('_V')


class _LateBound(NamedTuple):
    actual: Any


def late(o: _T | Iterator[_V] | Callable[[], _R]) -> _T | _V | _R:
    if isinstance(o, int | float | str | bytes | bool | tuple | bytearray | frozenset):
        return o  # type: ignore

    return _LateBound(actual=o)  # type: ignore


__ = late


__ = late


def _lateargs(func: Callable, **kwargs) -> dict[str, Any]:

    def resolve_default(value):
        if isinstance(value, Iterator):
            return next(value)
        if inspect.isfunction(value):
            return value()
        return copy.deepcopy(value)

    lateargs = {
        name: resolve_default(param.default.actual)
        for name, param in inspect.signature(func).parameters.items()
        if name not in kwargs and isinstance(param.default, _LateBound)
    }
    return {**kwargs, **lateargs}


def latebinding(target):
    if type(target) is type:
        return _latebindclass(target)

    @functools.wraps(target)
    def wrapper(*args, **kwargs):
        kwargs = _lateargs(target, **kwargs)
        return target(*args, **kwargs)

    return wrapper


def _latebindclass(cls):
    old_init = cls.__init__

    @functools.wraps(old_init)
    def new_init(self, *args, **kwargs):
        kwargs = _lateargs(old_init, **kwargs)
        old_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
