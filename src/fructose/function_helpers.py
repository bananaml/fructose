import inspect
from typing import Any, Callable
import typing

ALLOWED_PARAMETER_KINDS = [
    inspect.Parameter.POSITIONAL_OR_KEYWORD,
    inspect.Parameter.KEYWORD_ONLY
]


def collect_arguments(func, args, kwargs) -> dict[str, Any]:
    """
    Collects all arguments for a function, including default values and returns them as a dictionary.
    """

    signature = inspect.signature(func)

    arguments = {}
    for name, param in signature.parameters.items():
        if param.kind not in ALLOWED_PARAMETER_KINDS:
            raise ValueError(f"Unsupported parameter kind: {param.kind}")
        if name in kwargs:
            arguments[name] = kwargs[name]
        elif args and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            arguments[name] = args[0]
            args = args[1:]
        else:
            arguments[name] = param.default

    return arguments

def _convert_type_to_openai_type(type_: type) -> dict[str, Any]:
    _lookup = {
        str: "string",
        int: "number",
        float: "number",
        list: "array",
        dict: "object",
        bool: "boolean"
    }

    openai_type = {}

    origined_type = typing.get_origin(type_) or type_
    if origined_type in _lookup:
        name = _lookup[origined_type]
        openai_type["type"] = name
    else:
        raise ValueError(f"Unsupported type: {type_}")

    if origined_type == list:
        args = typing.get_args(type_)
        openai_type["items"] = _convert_type_to_openai_type(args[0])

    if origined_type == dict:
        args = typing.get_args(type_)
        openai_type["additionalProperties"] = _convert_type_to_openai_type(args[1])

    return openai_type


def convert_function_to_openai_function(func: Callable) -> dict[str, Any]:
    """
    Converts a function to an OpenAI function.
    """
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    name: _convert_type_to_openai_type(param.annotation)
                    for name, param in inspect.signature(func).parameters.items()
                }
            }
        }
    }
