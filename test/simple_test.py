import inspect
from typing import Any

from late import latebinding, 包


def test_with_list():

    @latebinding
    def f(x: list[Any] = []) -> list[Any]:
        x.append(1)
        return x

    assert f() == [1]
    assert f() == [1]
    assert f() == [1]


def test_immutable():
    @latebinding
    def f(x: frozenset[Any] = frozenset(), y: set = set()):
        return

    param = inspect.signature(f).parameters['x']
    assert type(param.default) is frozenset
    param = inspect.signature(f).parameters['y']
    assert type(param.default) is set


def test_kanji():
    @latebinding
    def f(x: list[Any] = 包([])) -> list[Any]:
        x.append(1)
        return x

    assert f() == [1]
    assert f() == [1]
