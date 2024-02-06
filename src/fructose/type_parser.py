import types
from typing import Dict, List, Set, Tuple
import inspect
import dataclasses
from typing import get_type_hints

_primitive_types = set([int, str, float, bool])
_wrapper_types = set([List, Dict, Tuple, Set])

class InvalidTypeException(Exception):
    pass

class EmptyReturnException(Exception):
    pass

def validate_return_type(func_name, return_type):
    if return_type is inspect.Signature.empty:
        raise EmptyReturnException(f"Return type for {func_name} is Empty. Please add a return type with this notation: def {func_name}(...) -> your_return_type:" )

    if not (return_type in _primitive_types or dataclasses.is_dataclass(return_type)):
        raise NotImplementedError("Fructose does not support return type " + type_to_string(return_type) + " yet. Please use int, str, float, or bool.")

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

def describe_dataclass_as_dict(cls) -> dict:
    if not dataclasses.is_dataclass(cls):
        raise ValueError(f"{cls.__name__} is not a dataclass.")
    
    type_hints = get_type_hints(cls)
    
    description = {}
    for field in dataclasses.fields(cls):
        field_type = type_hints[field.name]
        description[field.name] = str(field_type.__name__)
    
    return description


