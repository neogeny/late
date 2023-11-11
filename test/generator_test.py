from typing import Iterator
from late import latebinding, __, _LateBound


def test_generator():

    def fib() -> Iterator[int]:
        x, y = 0, 1
        while True:
            yield x
            x, y = y, x + y


    @latebinding
    def f(x: int = __(fib())) -> int:
        return x

    assert f() == 0
    assert f() == 1
    assert f() == 1
    assert f() == 2
    assert f() == 3
    assert f() == 5
