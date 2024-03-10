from functools import wraps
import os
from typing import Any, Callable, Optional
from pathlib import Path
from .llm_function_handler import LLMFunctionHandler
import openai
from jinja2 import Environment, FileSystemLoader, StrictUndefined

DEFAULT_MODEL = "gpt-4-turbo-preview"
# DEFAULT_MODEL = "gpt-3.5-turbo"

LabeledArguments = dict[str, Any]

def get_base_template_env():
    p = Path(__file__).parent / 'templates'
    loader = FileSystemLoader(p)

    return Environment(
        loader=loader,
        undefined=StrictUndefined
    )

def get_local_template_loader():
    loader = FileSystemLoader(searchpath="./")
    return Environment(
        loader=loader,
        undefined=StrictUndefined
    )

class Fructose():
    def __init__(self, client=None, model=DEFAULT_MODEL, system_template_path=None, chain_of_thought_template_path=None, debug=False):
        if client is None:
            client = openai.Client(
                api_key=os.environ['OPENAI_API_KEY'],
                base_url=os.environ.get('OPENAI_BASE_URL', None),
            )
        self._client = client
        self._model = model
        self._system_template_path = system_template_path
        self._chain_of_thought_template_path = chain_of_thought_template_path
        self._debug = debug

    def __call__(
            self,
            func: Optional[Callable] = None,
            *, # Enforce keyword-only arguments
            uses=[],
            flavors=[],
            system_template_path=None,
            chain_of_thought_template_path=None,
            model=None,
            debug=False,
        ):

        if func is not None and callable(func):
            # This means the decorator is used without parentheses, provide default args
            return self.__call__(
                uses=uses,
                flavors=flavors,
                system_template_path=system_template_path,
                chain_of_thought_template_path=chain_of_thought_template_path,
                model=model,
                debug=debug
            )(func)

        if debug is None:
            debug = self._debug
        model = model or self._model

        system_template_path = system_template_path or self._system_template_path
        chain_of_thought_template_path = chain_of_thought_template_path or self._chain_of_thought_template_path

        if system_template_path is not None:
            system_template = get_base_template_env().get_template(system_template_path)
        else:
            system_template = get_base_template_env().get_template("default_prompt.jinja")

        if chain_of_thought_template_path is not None:
            chain_of_thought_template = get_base_template_env().get_template(chain_of_thought_template_path)
        else:
            chain_of_thought_template = get_base_template_env().get_template("chain_of_thought_prompt.jinja")

        def decorator(func):
            llm_function_handler = LLMFunctionHandler(
                client=self._client,
                model=model,
                func=func,
                uses=uses,
                flavors=flavors,
                system_template=system_template,
                chain_of_thought_template=chain_of_thought_template,
                debug=debug)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return llm_function_handler(*args, **kwargs)
           
            return wrapper
        
        return decorator
