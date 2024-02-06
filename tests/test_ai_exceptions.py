from fructose import Fructose, type_parser
import pytest

AI = Fructose()

# We test known exceptions to ensure that the AI decorator is working as expected.

def test_none2none():
    with pytest.raises(type_parser.EmptyReturnException):
        @AI()
        def none2none():
            """
            Return absolutely nothing.
            """