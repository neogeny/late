from typing import Any

from late import latebinding, __


def test_recursion():
    @latebinding
    def f(x: list[list[Any]] = __([[]])) -> list[list[Any]]:
        x[0].append(1)
        return x

    assert f() == [[1]]
    assert f() == [[1]]


def test_function():
    t = 0

    def a() -> int:
        nonlocal t
        t += 1
        return t

    @latebinding
    def f(x: int = __(a)) -> int:
        return 2 * x

    assert f() == 2
    assert f() == 4
