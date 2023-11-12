import copy
import functools
import inspect
from typing import Any, Callable, Iterator, NamedTuple, TypeVar


__all__ = ['latebinding', 'late', '__']


_T = TypeVar('_T')
_V = TypeVar('_V')


class _LateBound(NamedTuple):
    actual: Any


def late(o: _T | Iterator[_V]) -> _T | _V:
    if isinstance(o, int | float | str | bool | bytes | bytearray | frozenset):
        return o  # type: ignore

    actual: Any = None
    if isinstance(o, list):
        actual = [late(value) for value in o]
    elif isinstance(o, dict):
        actual = {name: late(value) for name, value in o.items()}
    elif isinstance(o, set):
        actual = {late(value) for value in o}
    else:
        actual = o
    return _LateBound(actual=actual)  # type: ignore


__ = late


__ = late


def _lateargs(func: Callable, **kwargs) -> dict[str, Any]:

    def resolve_default(value):
        if inspect.isgenerator(value):
            return next(value)
        if inspect.isfunction(value):
            return value()
        if isinstance(value, _LateBound):
            return resolve_default(value.actual)
        if isinstance(value, list):
            return [resolve_default(x) for x in value]
        if isinstance(value, dict):
            return {name: resolve_default(x) for name, x in value.items()}
        if isinstance(value, set):
            return {resolve_default(x) for x in value}
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
