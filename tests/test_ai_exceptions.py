from fructose import AI, type_parser
import pytest

# We test known exceptions to ensure that the AI decorator is working as expected.

def test_none2none():
    with pytest.raises(type_parser.NoneReturnException):
        @AI()
        def none2none():
            """
            Return absolutely nothing.
            """