import types
from typing import get_origin, get_type_hints, Any, get_args
import inspect
import dataclasses

_primitive_types = set([int, str, float, bool])
_wrapper_types = set([list, dict])

class InvalidTypeException(Exception):
    pass

class EmptyReturnException(Exception):
    pass

def is_supported_return_type(return_type):
    """
    Check if the return type is supported by Fructose.
    The supported types are the primitive types & wrapper types and dataclasses.
    """

    # Check if the return_type is directly one of the primitive types or a dataclass
    if return_type in _primitive_types or dataclasses.is_dataclass(return_type):
        return True
    
    # Determine the origin type for generic types or use the return_type itself for non-generic types
    origin = get_origin(return_type) or return_type

    # Small hack to not support the typing module, better to catch it here than to let users do the LLM call
    # and then get an error.
    try:
        if return_type.__module__ == "typing":
            return False
    except:
        pass

    # Check if the origin type is supported
    if origin in _wrapper_types:
        # Ensure all argument types for generic types are supported
        args = get_args(return_type)
        return all(is_supported_return_type(arg) for arg in args) if args else True

    # If none of the above conditions are met, the type is not supported
    return False

### Validate the that the return from the LLM is a valid type ###

def perform_type_validation(value: Any, expected_type: Any):
    """
    Validates that the output of the LLM is a valid type and the one expected by the decorated function.
    """
    if expected_type is Any:
        return
    actual_type = type(value)

    root_expected_type = get_origin(expected_type) or expected_type

    is_valid = True

    # in python bool is a subclass of int, so we need to check for this case
    if root_expected_type == int and actual_type == bool:
        is_valid = False
    if not isinstance(value, root_expected_type):
        is_valid = False

    if not is_valid:
        raise ValueError(f"Expected value of type {root_expected_type}, but got type {actual_type}")

    # handle wrapper types
    if root_expected_type == list:
        inner_type = (get_args(expected_type) or (Any,))[0]

        for item in value:
            perform_type_validation(item, inner_type)

    if root_expected_type == dict:
        key_type, val_type = (get_args(expected_type) or (Any, Any))

        for k, v in value.items():
            perform_type_validation(k, key_type)
            perform_type_validation(v, val_type)

    # handle dataclasses
    if dataclasses.is_dataclass(root_expected_type):
        for field in dataclasses.fields(root_expected_type):
            field_value = getattr(value, field.name)
            perform_type_validation(field_value, field.type)

def _describe_dataclass_as_dict(cls) -> dict:
    if not dataclasses.is_dataclass(cls):
        raise ValueError(f"{cls.__name__} is not a dataclass.")
    
    type_hints = get_type_hints(cls)
    
    description = {}
    for field in dataclasses.fields(cls):
        description[field.name] = type_to_string(type_hints[field.name])
    
    return description

def type_to_string(my_type):
    if not type(my_type) in [type, types.GenericAlias]:
        raise InvalidTypeException(f"Invalid type: {my_type}")


    if dataclasses.is_dataclass(my_type):
        description =  _describe_dataclass_as_dict(my_type)
        result = "{" + \
            ", ".join([f"{k}: {v}" for k, v in description.items()]) + \
            "}"
        return result
    else:
        prefix = my_type.__name__

        if hasattr(my_type, "__args__"):
            args = getattr(my_type, "__args__")
            formatted_args = [type_to_string(arg) for arg in args]
            return f"{prefix}[{', '.join(formatted_args)}]"
        else:
            return prefix
