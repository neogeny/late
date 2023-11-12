from itertools import count

from late import latebinding, __


def test_iterator():

    @latebinding
    def f(x: int = __(count(start=7))):
        return x

    assert f() == 7
    assert f() == 8
