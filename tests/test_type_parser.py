from typing import List
from dataclasses import dataclass

import pytest
from fructose import type_parser

@dataclass
class Person:
    name: str
    age: int
    items: list[tuple[ str, int ]]

@dataclass
class Company:
    name: str
    employees: list[Person]




def test_to_string():
    assert type_parser.type_to_string(int) == 'int'
    assert type_parser.type_to_string(str) == 'str'
    assert type_parser.type_to_string(float) == 'float'
    assert type_parser.type_to_string(bool) == 'bool'

    assert type_parser.type_to_string(list[int]) == 'list[int]'
    assert type_parser.type_to_string(list[list[int]]) == 'list[list[int]]'

    # test for dict, set, and tuple
    assert type_parser.type_to_string(dict[str, int]) == 'dict[str, int]'
    assert type_parser.type_to_string(set[str]) == 'set[str]'
    assert type_parser.type_to_string(tuple[str, int]) == 'tuple[str, int]'
    assert type_parser.type_to_string(tuple[str, int, float]) == 'tuple[str, int, float]'

    # combine all
    assert type_parser.type_to_string(dict[str, list[tuple[str, int]]]) == 'dict[str, list[tuple[str, int]]]'


    assert type_parser.type_to_string(Person) == '{name: str, age: int, items: list[tuple[str, int]]}'
    assert type_parser.type_to_string(list[Person]) == 'list[{name: str, age: int, items: list[tuple[str, int]]}]'


    assert type_parser.type_to_string(Company) == '{name: str, employees: list[{name: str, age: int, items: list[tuple[str, int]]}]}'

def test_perform_type_validation():
    type_parser.perform_type_validation(1, int)
    type_parser.perform_type_validation('1', str)
    type_parser.perform_type_validation(1.0, float)
    type_parser.perform_type_validation(True, bool)
    type_parser.perform_type_validation([1, 2, 3], list[int])
    type_parser.perform_type_validation(["1", "2", "3"], list[str])
    type_parser.perform_type_validation([1.0, 2.0, 3.0], list[float])
    type_parser.perform_type_validation([True, False, True], list[bool])
    type_parser.perform_type_validation({"a": 1, "b": 2}, dict[str, int])
    type_parser.perform_type_validation({"a": [1, 2, 3], "b": [4, 5, 6]}, dict[str, list[int]])
    type_parser.perform_type_validation({"a": [Company(name="a", employees=[Person(name="a", age=1, items=[("a", 1)])])]}, dict[str, list[Company]])
    # test implicit any
    type_parser.perform_type_validation({"asdf": 1, 1: "asdf"}, dict)
    type_parser.perform_type_validation([1, "asdf"], list)

    with pytest.raises(ValueError):
        type_parser.perform_type_validation(1, str)
    with pytest.raises(ValueError):
        type_parser.perform_type_validation('1', int)
    with pytest.raises(ValueError):
        type_parser.perform_type_validation(1.0, int)
    with pytest.raises(ValueError):
        type_parser.perform_type_validation(True, int)
    with pytest.raises(ValueError):
        type_parser.perform_type_validation([1, 2, 3], list[str])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation(["1", "2", "3"], list[int])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation([1.0, 2.0, 3.0], list[int])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation([True, False, True], list[int])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation({"a": 1, "b": 2}, dict[int, str])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation({"a": [1, 2, 3], "b": [4, 5, 6]}, dict[str, list[str]])
    with pytest.raises(ValueError):
        type_parser.perform_type_validation({"a": [Company(name="a", employees=[Person(name=1, age=1, items=[("a", 1)])])]}, dict[str, list[Company]]) #type: ignore


def test_supported_types():

    # support for primitive types
    assert type_parser.is_supported_return_type(int) == True
    assert type_parser.is_supported_return_type(str) == True
    assert type_parser.is_supported_return_type(float) == True
    assert type_parser.is_supported_return_type(bool) == True

    # support for generic types
    assert type_parser.is_supported_return_type(list[int]) == True
    assert type_parser.is_supported_return_type(list) == True
    assert type_parser.is_supported_return_type(list[list[int]]) == True
    assert type_parser.is_supported_return_type(dict[str, int]) == True

    assert type_parser.is_supported_return_type(Person) == True
    assert type_parser.is_supported_return_type(list[Person]) == True

    # not supported types
    assert type_parser.is_supported_return_type(type(None)) == False
    assert type_parser.is_supported_return_type(list[object]) == False
    assert type_parser.is_supported_return_type(list[None]) == False
    assert type_parser.is_supported_return_type(List) == False
    assert type_parser.is_supported_return_type(List[str]) == False

    # tuples and sets are not supported yet
    assert type_parser.is_supported_return_type(set[str]) == False
    assert type_parser.is_supported_return_type(tuple[str, int]) == False
    assert type_parser.is_supported_return_type(tuple[str, int, float]) == False


    
