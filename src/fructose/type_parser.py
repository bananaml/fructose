import types
from typing import Dict, List, Set, Tuple


_primitive_types = set([int, str, float, bool])

_wrapper_types = set([List, Dict, Tuple, Set])

class InvalidTypeException(Exception):
    pass

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



