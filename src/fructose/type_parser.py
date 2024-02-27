from enum import Enum
import types
from typing import Union, get_origin, get_type_hints, Any, get_args
import dataclasses

_primitive_types = set([int, str, float, bool])
_wrapper_types = set([list, dict, tuple])

class InvalidTypeException(Exception):
    pass

class EmptyReturnException(Exception):
    pass

def _is_supported_dataclass(cls):
    if not dataclasses.is_dataclass(cls):
        return False

    # Check if all fields are supported

    for field in dataclasses.fields(cls):
        if not is_supported_return_type(field.type):
            return False

    return True

def _is_enum(cls):
    try:
        return issubclass(cls, Enum)
    except:
        return False

def _is_optional(tp):
    """
    Check if a type is Optional or Union with exactly two arguments.

    :param tp: The type to check.
    :return: True if the type is Union with exactly two arguments, False otherwise.
    """
    origin = get_origin(tp)
    if origin is Union:
        args = get_args(tp)
        if len(args) ==  2 and any(arg is type(None) for arg in args):
            return True
    return False

def _is_supported_wrapper_type(return_type):
    origin = get_origin(return_type)
    if origin not in _wrapper_types:
        return False

    # Small hack to not support the typing module, better to catch it here than to let users do the LLM call
    # and then get an error.
    try:
        if return_type.__module__ == "typing":
            return False
    except:
        pass

    args = get_args(return_type)

    if not args:
        return False

    # for now we only support keys of type str and values of any type
    if origin == dict and args[0] != str:
        return False

    return all(is_supported_return_type(arg) for arg in args)

def is_supported_return_type(return_type):
    """
    Check if the return type is supported by Fructose.
    The supported types are the primitive types & wrapper types and dataclasses.
    """

    return any([
        return_type in _primitive_types,
        _is_supported_dataclass(return_type),
        _is_enum(return_type),
        _is_optional(return_type),
        _is_supported_wrapper_type(return_type),
    ])

def _parse_tuple(json_result, return_type: type[tuple]):
    if type(json_result) != list:
        raise ValueError(f"Value {json_result} is not of type {list}")
    typed_tuple = []
    sub_types = get_args(return_type)
    if not sub_types:
        return tuple(json_result)
    for item, sub_type in zip(json_result, sub_types):
        item = parse_json_to_type(item, sub_type)
        typed_tuple.append(item)

    return tuple(typed_tuple)

def _parse_list(json_result, return_type: type[list]):
    if type(json_result) != list:
        raise ValueError(f"Value {json_result} is not of type {list}")
    typed_list = []
    sub_type = get_args(return_type)[0]
    for item in json_result:
        item = parse_json_to_type(item, sub_type)
        typed_list.append(item)

    return typed_list

def _parse_dict(json_result, return_type: type[dict]):
    key_type, val_type = get_args(return_type)
    typed_dict = {}
    for key, val in json_result.items():
        typed_key = parse_json_to_type(key, key_type)
        typed_val = parse_json_to_type(val, val_type)
        typed_dict[typed_key] = typed_val

    return typed_dict

def _parse_enum(json_result, enum):
    if type(json_result) != str:
        raise ValueError(f"Value {json_result} is not of type {str}")

    # match enum on name
    for member in enum:
        if member.name == json_result:
            return member

    raise ValueError(f"Value {json_result} is not a valid member of {enum}")

def _parse_optional(json_result, return_type: type[Union]):
    args = get_args(return_type)
    if len(args) != 2 or not any(arg is type(None) for arg in args) or all(arg is type(None) for arg in args):
        raise ValueError(f"Union type {return_type} is not supported by Fructose.")

    if json_result is None:
        return None

    sub_type = next(arg for arg in args if arg is not type(None))
    return parse_json_to_type(json_result, sub_type)

_json_type_parser_lookup = {
    list: _parse_list,
    dict: _parse_dict,
    tuple: _parse_tuple,
    Union: _parse_optional,
}

def _parse_dataclass(json_result, return_type):
    if type(json_result) != dict:
        raise ValueError(f"Value {json_result} is not of type {dict}")
    args = {}
    for field in dataclasses.fields(return_type):
        field_name = field.name
        field_type = field.type
        args[field_name] = parse_json_to_type(json_result[field_name], field_type)

    return return_type(**args)

def parse_json_to_type(json_result: dict, return_type: Any) -> Any:
    """
    Parse a JSON object to a given type.
    """
    assert is_supported_return_type(return_type), f"Type {return_type} is not supported by Fructose."
    origin = get_origin(return_type) or return_type

    if origin in _json_type_parser_lookup:
        return _json_type_parser_lookup[origin](json_result, return_type)
    elif _is_enum(return_type):
        return _parse_enum(json_result, return_type)
    elif dataclasses.is_dataclass(return_type):
        return _parse_dataclass(json_result, return_type)
    elif return_type in _primitive_types:
        casted_result = return_type(json_result)
        if casted_result != json_result:
            raise ValueError(f"Value {json_result} is not of type {return_type}")
        # bool is a special case since it's a subclass of int
        if bool in [return_type, type(json_result)] and type(json_result) != return_type:
            raise ValueError(f"Value {json_result} is not of type {return_type}")
        return casted_result

    raise InvalidTypeException(f"Type {return_type} is not supported by Fructose")


def _describe_dataclass_as_dict(cls) -> dict:
    if not dataclasses.is_dataclass(cls):
        raise ValueError(f"{cls.__name__} is not a dataclass.")
    
    type_hints = get_type_hints(cls)
    
    description = {}
    for field in dataclasses.fields(cls):
        description[field.name] = type_to_string(type_hints[field.name])
    
    return description

def _enum_to_string(tp):
    members = [f'"{member.name}"' for member in tp]
    return f"str[{' | '.join(members)}]"

def _dataclass_to_string(tp):
    description =  _describe_dataclass_as_dict(tp)
    result = "{" + \
        ", ".join([f"{k}: {v}" for k, v in description.items()]) + \
        "}"
    return result

def _primitive_to_string(tp) -> str:
    return tp.__name__

def _wrapper_to_string(tp):
    prefix = tp.__name__
    args = getattr(tp, "__args__")
    if not args:
        raise InvalidTypeException(f"Invalid type: {tp}")
    formatted_args = [type_to_string(arg) for arg in args]
    return f"{prefix}[{', '.join(formatted_args)}]"

def _optional_to_string(tp):
    types = tp.__args__
    optional_type = [t for t in types if t != type(None)][0]
    optional_type_str = type_to_string(optional_type)
    return f"Optional[{optional_type_str}]"


def type_to_string(my_type) -> str:
    if _is_enum(my_type):
        return _enum_to_string(my_type)
    if dataclasses.is_dataclass(my_type):
        return _dataclass_to_string(my_type)
    if _is_optional(my_type):
        return _optional_to_string(my_type)
    if my_type in _primitive_types:
        return _primitive_to_string(my_type)
    if _is_supported_wrapper_type(my_type):
        return _wrapper_to_string(my_type)

    raise InvalidTypeException(f"Invalid type: {my_type}")
