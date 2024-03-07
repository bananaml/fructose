from dataclasses import dataclass
import re
from typing import Optional
from fructose import Fructose
ai = Fructose()

# In all cases, we assert the return type

# In trivial cases that the LLM shouldn't mess up on, we assert the return value. 
# NOTE: this adds flakiness to the tests. But Fructose would be a useless package if we couldn't trust trivial cases. 


# ----
# Type - to - Type tests

def test_str2str():
    @ai()
    def echo(words: str) -> str:
        """
        Repeat the input string back to the user.
        """
        ...
    
    res = echo("onomatopoeia")
    assert type(res) == str
    assert res == "onomatopoeia"
    

def test_str2int():
    @ai()
    def len_str(words: str) -> int:
        """
        Return the length of the input string.
        """
        ...
    
    res = len_str("onomatopoeia")
    assert type(res) == int


def test_none2int():
    @ai()
    def none2int() -> int:
        """
        Return the integer 42.
        """
        ...
    
    res = none2int()
    assert res == 42
    assert type(res) == int

def test_none2str():
    @ai()
    def none2str() -> str:
        """
        Return the string "42".
        """
        ...
    
    res = none2str()
    assert res == "42"
    assert type(res) == str

def test_none2float():
    @ai()
    def none2float() -> float:
        """
        Return the float 42.0.
        """
        ...
    
    res = none2float()
    assert res == 42.0
    assert type(res) == float

def test_none2bool():
    @ai()
    def none2bool() -> bool:
        """
        Return the boolean True.
        """
        ...
    
    res = none2bool()
    assert res == True
    assert type(res) == bool

def test_bool2bool():
    @ai(debug=True)
    def bool2bool(boolean: bool) -> bool:
        """
        Return the input boolean value.
        """
        ...
    
    res = bool2bool(True)
    assert res == True
    assert type(res) == bool

    res = bool2bool(False)
    assert res == False
    assert type(res) == bool

def test_bool2int():
    @ai()
    def bool2int(boolean: bool) -> int:
        """
        Return an integer, 1 if the input is True, 0 if the input is False.
        Valid return values are 1 and 0.
        """
        ...
    
    res = bool2int(True)
    assert res == 1
    assert type(res) == int

    res = bool2int(False)
    assert res == 0
    assert type(res) == int

def test_bool2str():
    @ai()
    def bool2str(boolean: bool) -> str:
        """
        Return the string "TRUE" if the input is True, "FALSE" if the input is False. It must be in all caps.
        """
        ...
    
    res = bool2str(True)
    assert res == "TRUE"
    assert type(res) == str

    res = bool2str(False)
    assert res == "FALSE"
    assert type(res) == str

def test_listint2int():
    @ai()
    def listint2listint(numbers: list[int]) -> int:
        """
        Return the first integer in the list.
        """
        ...
    
    res = listint2listint([1, 2, 3])
    assert res == 1
    assert type(res) == int

def test_optional():
    @ai()
    def maybe_get_int(instructions: str) -> Optional[int]:
        """
        based on the given instructions, decides to return an int or not
        """
        ...

    result = maybe_get_int("give me the number 5")
    assert result == 5
    result = maybe_get_int("don't give me a number")
    assert result == None


# ----
# Mixed Args KWArgs tests

def test_kwargs():
    @ai()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """
        ...

    res = logical_and(bool1 = True, bool2 = False)
    assert res == False
    assert type(res) == bool

def test_mixed_order_kwargs():
    @ai()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """
        ...

    res = logical_and(bool2 = False, bool1 = True)
    assert res == False
    assert type(res) == bool

def test_mixed_positional_kwargs():
    @ai()
    def logical_and(bool1: bool, bool2: bool) -> bool:
        """
        Return the logical AND of the two input booleans.
        """
        ...
        
    # mixed positional and kwargs
    res = logical_and(True, bool2 = False)
    assert res == False
    assert type(res) == bool

def test_uses_add_function():
    add_called = False
    def add(a: int, b: int) -> int:
        """
        Return the sum of the two input integers.
        """
        nonlocal add_called
        add_called = True
        return a + b

    @ai(uses=[add], debug=True)
    def add_two_numbers(a: int, b: int) -> int:
        """
        Return the sum of the two input integers.
        """
        ...

    res = add_two_numbers(1, 2)
    assert res == 3
    assert add_called == True


def test_uses_regex_function():
    regex_matches_called = False
    def regex_matches(pattern: str, strings: list[str]) -> bool:
        """
        Return True if the pattern matches all the strings, False otherwise.
        """
        nonlocal regex_matches_called
        regex_matches_called = True

        for string in strings:
            if not bool(re.match(pattern, string)):
                return False
        return True

    @ai(uses=[regex_matches], debug=True)
    def generate_regex(positive_examples: list[str], negative_examples: list[str]) -> str:
        """
        Return a regex pattern that matches all the positive example strings. Uses regex_matches to validate the result before returning a final result.
        """
        ...

    result = generate_regex(["hello", "world"], ["HELLO", "WORLD"])

    assert regex_matches_called == True
    assert regex_matches(result, ["hello", "world"])
    assert not regex_matches(result, ["HELLO", "WORLD"])


# ----
# Python quirks
    
def test_decorator_without_args():
    @ai
    def add(a: int, b: int) -> int:
        """
        Return the sum of the two input integers.
        """
        ...
    
    res = add(1, 2)
    assert res == 3
    assert type(res) == int

@dataclass
class Point:
    x: int
    y: int

    @staticmethod
    @ai()
    def generate_point() -> "Point":
        """
        Return a random point.
        """
        ...

def test_forward_ref_type_parser():
    res = Point.generate_point()
    assert type(res) == Point
