import copy
import functools
import inspect
from typing import Any, NamedTuple, TypeVar


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


def latebinding(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        lateargs = {
            name: copy.copy(param.default.actual)
            for name, param in inspect.signature(func).parameters.items()
            if name not in kwargs and isinstance(param.default, _LateBound)
        }
        kwargs.update(lateargs)

        return func(*args, **kwargs)

    return wrapper
