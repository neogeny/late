from dataclasses import dataclass
from typing import Any

from late import __, latebinding


def test_dataclass():

    @latebinding
    @dataclass
    class C:
        x: list[Any] = __([])

    c = C()
    assert c.x == []

    d = C()
    assert d.x == []
    c.x = [1]
    assert c.x == [1]
    assert d.x == []

    assert d.x is not c.x
