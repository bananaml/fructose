from typing import List
from dataclasses import dataclass
from fructose import type_parser

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

def test_supported_types():

    # support for primitive types
    assert type_parser.is_supported_type(int) == True
    assert type_parser.is_supported_type(str) == True
    assert type_parser.is_supported_type(float) == True
    assert type_parser.is_supported_type(bool) == True

    # support for generic types
    assert type_parser.is_supported_type(list[int]) == True
    assert type_parser.is_supported_type(list) == True
    assert type_parser.is_supported_type(list[list[int]]) == True
    assert type_parser.is_supported_type(dict[str, int]) == True

    # support for dataclass
    @dataclass
    class Person:
        pass
    
    assert type_parser.is_supported_type(Person) == True
    assert type_parser.is_supported_type(list[Person]) == True

    # not supported types
    assert type_parser.is_supported_type(type(None)) == False
    assert type_parser.is_supported_type(list[object]) == False
    assert type_parser.is_supported_type(list[None]) == False
    assert type_parser.is_supported_type(List) == False
    assert type_parser.is_supported_type(List[str]) == False

    # tuples and sets are not supported yet
    assert type_parser.is_supported_type(set[str]) == False
    assert type_parser.is_supported_type(tuple[str, int]) == False
    assert type_parser.is_supported_type(tuple[str, int, float]) == False


    