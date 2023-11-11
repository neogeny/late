import copy
import functools
import inspect
from typing import Any, Callable, NamedTuple, TypeVar


__all__ = ['latebinding', 'late', '__']


_T = TypeVar('_T')


class _LateBound(NamedTuple):
    actual: Any


def late(o: _T) -> _T:
    if isinstance(o, int | float | str | bool | bytes | bytearray | frozenset):
        return o
    else:
        return _LateBound(actual=o)  # type: _T


__ = late


def _lateargs(func: Callable, **kwargs) -> dict[str, Any]:
    lateargs = {
        name: copy.copy(param.default.actual)
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
