import inspect
from typing import Any

from late import latebinding, __, _LateBound


def test_with_list():

    @latebinding
    def f(x: list[Any] = __([])) -> list[Any]:
        x.append(1)
        return x

    assert f() == [1]
    assert f() == [1]
    assert f() == [1]


def test_immutable():
    @latebinding
    def f(x: list[Any] = __(frozenset()), y: set = __({})) -> list[Any]:
        x.append(1)
        return x

    param = inspect.signature(f).parameters['x']
    assert type(param.default) is frozenset
    param = inspect.signature(f).parameters['y']
    assert type(param.default) is _LateBound
