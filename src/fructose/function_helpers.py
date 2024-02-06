import inspect
from typing import Any

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
