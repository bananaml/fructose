from fructose import Fructose
from dataclasses import dataclass

ai = Fructose()

def test_parse_llm_result():

    # primitive success cases
    assert ai._parse_llm_result('{"final_response": "Hello, world!"}', str) == "Hello, world!"
    assert ai._parse_llm_result('{"final_response": 42}', int) == 42
    assert ai._parse_llm_result('{"final_response": 3.14}', float) == 3.14
    assert ai._parse_llm_result('{"final_response": true}', bool) == True
    assert ai._parse_llm_result('{"final_response": false}', bool) == False

    # generic success cases
    assert ai._parse_llm_result('{"final_response": [1, 2, 3]}', list) == [1, 2, 3]
    assert ai._parse_llm_result('{"final_response": [1, 2, 3]}', list[int]) == [1, 2, 3]
    assert ai._parse_llm_result("{\"final_response\": {\"a\": 1, \"b\": 2}}", dict[str, int]) == {"a": 1, "b": 2}

    # dataclass success cases
    @dataclass
    class MyDataclass:
        a: int
        b: int

    assert ai._parse_llm_result('{\"final_response\": {\"a\": 1, \"b\": 2}}', MyDataclass) == MyDataclass(a=1, b=2)

    # edge cases -- especially "False" with a capital F is a common failure case
    assert ai._parse_llm_result('{"final_response": "False"}', bool) == False