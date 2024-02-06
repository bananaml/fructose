import pytest
from fructose.function_helpers import collect_arguments

def test_collect_arguments():
    def test_function(a, b, c=3, d=4):
        pass

    args = [1, 2]
    kwargs = {'d': 5}
    result = collect_arguments(test_function, args, kwargs)
    assert result == {'a': 1, 'b': 2, 'c': 3, 'd': 5}
