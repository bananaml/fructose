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