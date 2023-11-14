import inspect
from typing import Any

from late import __, _LateBound, latebinding, 包


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
    def f(x: frozenset[Any] = __(frozenset()), y: set = __(set())):
        return

    param = inspect.signature(f).parameters['x']
    assert type(param.default) is frozenset
    param = inspect.signature(f).parameters['y']
    assert type(param.default) is _LateBound


def test_kanji():
    @latebinding
    def f(x: list[Any] = 包([])) -> list[Any]:
        x.append(1)
        return x

    assert f() == [1]
    assert f() == [1]
