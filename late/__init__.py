import copy
import functools
import inspect
from typing import Any, Callable, Iterator, NamedTuple, TypeVar


__all__ = ['latebinding', 'late', '__']


_T = TypeVar('_T')
_V = TypeVar('_V')


class _LateBound(NamedTuple):
    actual: Any


def __(o: _T | Iterator[_V]) -> _T | _V:
    if isinstance(o, int | float | str | bool | bytes | bytearray | frozenset):
        return o  # type: ignore
    else:
        return _LateBound(actual=o)  # type: ignore


def _lateargs(func: Callable, **kwargs) -> dict[str, Any]:

    def resolve_default(value):
        if inspect.isgenerator(value):
            return next(value)
        return copy.copy(value)

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
