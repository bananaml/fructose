import types
from typing import Dict, List, Set, Tuple, get_origin, get_type_hints, Any, get_args
import inspect
import dataclasses
from collections.abc import Iterable, Mapping

_primitive_types = set([int, str, float, bool])
_wrapper_types = set([list, dict])

class InvalidTypeException(Exception):
    pass

class EmptyReturnException(Exception):
    pass

### Validate the return signature of the function ###

def validate_return_type_for_function(func_name, return_type):
    """
    Validates that the return type is supported by Fructose.
    """
    if return_type is inspect.Signature.empty:
        raise EmptyReturnException(f"Return type for {func_name} is Empty. Please add a return type with this notation: def {func_name}(...) -> your_return_type:")

    if not is_supported_type(return_type):
        raise NotImplementedError("Fructose does not support return type " + type_to_string(return_type) + " yet. Please use int, str, float, bool, or generic types.")


def is_supported_type(return_type):
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
        return all(is_supported_type(arg) for arg in args) if args else True

    # If none of the above conditions are met, the type is not supported
    return False

### Validate the that the return from the LLM is a valid type ###

def perform_type_validation(value: Any, expected_type: Any):
    """
    Validates that the output of the LLM is a valid type and the one expected by the decorated function.
    """

    # validate container types
    if get_origin(expected_type) or expected_type in _wrapper_types:
        validate_container_type(value, expected_type)

    # primitive types and dataclasses are validated directly 
    elif expected_type in _primitive_types or dataclasses.is_dataclass(expected_type):
        if not isinstance(value, expected_type):
            raise ValueError(f"Expected value of type {expected_type}, but got type {type(value)}")
    
    else:
        raise NotImplementedError(f"Type validation for {expected_type} is not implemented.")

def validate_container_type(value: Any, expected_type: Any):
    """
    Validates that container types have the correct type for their elements.
    If a type isn't specified for the internal elements, it will just check that outer container type is correct.
    """

    # Determine the origin of the expected type and its arguments
    expected_origin = get_origin(expected_type)
    expected_args = get_args(expected_type)

    if expected_origin and type(value) != expected_origin:
        raise ValueError(f"Type cast failed, value {value} is of type {type(value)}, expected {expected_origin}")

    if expected_args:
        
        if isinstance(value, Mapping):  # For dict-like objects
            key_type, val_type = expected_args
            for k, v in value.items():
                validate_container_type(k, key_type)
                validate_container_type(v, val_type)
        
        elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):  # For list, set, tuple (exclude str, bytes)
            item_type = expected_args[0]
            for item in value:
                validate_container_type(item, item_type)
    
    elif expected_origin:  # This handles non-generic types without __args__
        # Ensure the value matches the expected container type
        if not isinstance(value, expected_origin):
            raise ValueError(f"Type cast failed, value {value} is not of expected container type {expected_origin}")


### Helpers

def describe_dataclass_as_dict(cls) -> dict:
    if not dataclasses.is_dataclass(cls):
        raise ValueError(f"{cls.__name__} is not a dataclass.")
    
    type_hints = get_type_hints(cls)
    
    description = {}
    for field in dataclasses.fields(cls):
        field_type = type_hints[field.name]
        description[field.name] = str(field_type.__name__)
    
    return description

def type_to_string(my_type):
    if not type(my_type) in [type, types.GenericAlias]:
        raise InvalidTypeException(f"Invalid type: {my_type}")

    prefix = my_type.__name__
    
    if hasattr(my_type, "__args__"):
        args = getattr(my_type, "__args__")
        formatted_args = [type_to_string(arg) for arg in args]
        return f"{prefix}[{', '.join(formatted_args)}]"
    else:
        return prefix
