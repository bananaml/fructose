from typing import List
from enum import Enum
from dataclasses import dataclass

import pytest
from fructose import type_parser

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4

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

    # test for enum
    assert type_parser.type_to_string(Color) == '"RED" | "GREEN" | "BLUE"'
    assert type_parser.type_to_string(Weekday) == '"MONDAY" | "TUESDAY" | "WEDNESDAY" | "THURSDAY" | "FRIDAY"'

    # combine all
    assert type_parser.type_to_string(dict[str, list[tuple[str, int]]]) == 'dict[str, list[tuple[str, int]]]'

    assert type_parser.type_to_string(Person) == '{name: str, age: int, items: list[tuple[str, int]]}'
    assert type_parser.type_to_string(list[Person]) == 'list[{name: str, age: int, items: list[tuple[str, int]]}]'


    assert type_parser.type_to_string(Company) == '{name: str, employees: list[{name: str, age: int, items: list[tuple[str, int]]}]}'

def test_supported_types():

    # support for primitive types
    assert type_parser.is_supported_return_type(int) == True
    assert type_parser.is_supported_return_type(str) == True
    assert type_parser.is_supported_return_type(float) == True
    assert type_parser.is_supported_return_type(bool) == True

    # support for generic types
    assert type_parser.is_supported_return_type(list[int]) == True
    assert type_parser.is_supported_return_type(list[list[int]]) == True
    assert type_parser.is_supported_return_type(dict[str, int]) == True

    assert type_parser.is_supported_return_type(Person) == True
    assert type_parser.is_supported_return_type(list[Person]) == True
    assert type_parser.is_supported_return_type(tuple[str, int]) == True
    assert type_parser.is_supported_return_type(tuple[str, int, float]) == True

    # support for enums
    assert type_parser.is_supported_return_type(Color) == True
    assert type_parser.is_supported_return_type(Weekday) == True

    # not supported types
    assert type_parser.is_supported_return_type(list) == False
    assert type_parser.is_supported_return_type(type(None)) == False
    assert type_parser.is_supported_return_type(list[object]) == False
    assert type_parser.is_supported_return_type(list[None]) == False
    assert type_parser.is_supported_return_type(List) == False
    assert type_parser.is_supported_return_type(List[str]) == False

    # tuples and sets are not supported yet
    assert type_parser.is_supported_return_type(set[str]) == False

def test_parse_json_to_type():
    # test for primitive types
    assert type_parser.parse_json_to_type(1, int) == 1
    assert type_parser.parse_json_to_type("1", str) == "1"
    assert type_parser.parse_json_to_type(1.0, float) == 1.0
    assert type_parser.parse_json_to_type(True, bool) == True

    # test for list
    assert type_parser.parse_json_to_type([1, 2, 3], list[int]) == [1, 2, 3]
    assert type_parser.parse_json_to_type(["1", "2", "3"], list[str]) == ["1", "2", "3"]
    assert type_parser.parse_json_to_type([1.0, 2.0, 3.0], list[float]) == [1.0, 2.0, 3.0]
    assert type_parser.parse_json_to_type([True, False, True], list[bool]) == [True, False, True]

    # test for dict
    assert type_parser.parse_json_to_type({"a": 1, "b": 2}, dict[str, int]) == {"a": 1, "b": 2}
    assert type_parser.parse_json_to_type({"a": [1, 2, 3], "b": [4, 5, 6]}, dict[str, list[int]]) == {"a": [1, 2, 3], "b": [4, 5, 6]}

    # test for enums
    assert type_parser.parse_json_to_type("RED", Color) == Color.RED
    assert type_parser.parse_json_to_type("MONDAY", Weekday) == Weekday.MONDAY

    # test for custom types
    json = {"name": "a", "age": 1, "items": [["a", 1]]}
    expected = Person(name="a", age=1, items=[("a", 1)])
    assert type_parser.parse_json_to_type(json, Person) == expected

    expected = [Person(name="a", age=1, items=[("a", 1)])]
    json = [{"name": "a", "age": 1, "items": [["a", 1]]}]
    assert type_parser.parse_json_to_type(json, list[Person]) == expected

    # test for nested custom types
    expected = Company(name="a", employees=[Person(name="a", age=1, items=[("a", 1)])])
    json = {"name": "a", "employees": [{"name": "a", "age": 1, "items": [["a", 1]]}]}
    assert type_parser.parse_json_to_type(json, Company) == expected

    with pytest.raises(ValueError):
        type_parser.parse_json_to_type(1, str)
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type('1', int)
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type(1.5, int)
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type(True, int)
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type([1, 2, 3], list[str])
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type(["1", "2", "3"], list[int])
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type([1.5, 2.0, 3.0], list[int])
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type([True, False, True], list[int])
    with pytest.raises(ValueError):
        # test enum with wrong value
        type_parser.parse_json_to_type("RED", Weekday)
    with pytest.raises(ValueError):
        type_parser.parse_json_to_type({"a": [1, 2, 3], "b": [4, 5, 6]}, dict[str, list[str]])
    with pytest.raises(ValueError):
        return_type = dict[str, list[Company]]
        json_result = {"a": [
            {"name": "a", "employees": [{"name": 1, "age": 1, "items": [("a", 1)]}]}
        ]}
        type_parser.parse_json_to_type(json_result, return_type)



    
