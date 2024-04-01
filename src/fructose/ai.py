from functools import wraps
import os
from typing import Any, Callable, Optional
from pathlib import Path
from .llm_function_handler import LLMFunctionHandler
import openai
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import inspect

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

HUMAN_BASE_URL = os.getenv("HUMAN_BASE_URL", "https://human-production-571a.up.railway.app/")
human_first_call = True

class Fructose():
    def __init__(self, client=None, model=DEFAULT_MODEL, system_template_path=None, chain_of_thought_template_path=None, debug=False):
        if client is None:
            client = openai.Client(
                api_key=os.environ['OPENAI_API_KEY']
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
            debug=None,
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
        
        # TEMP: HUMAN MODE
        # we introspect callable name to see if human mode is enabled. incredibly hacky
        global human_first_call
        if human_first_call:
            # step back one frame and scan all local variables until we find this one
            # this is how we know the variable name
            caller_frame = inspect.currentframe().f_back
            for var_name, var_val in caller_frame.f_locals.items():
                if var_val is self:
                    if var_name == "human":
                        self._client=openai.Client(
                            api_key="not-needed",
                            base_url=HUMAN_BASE_URL,
                            max_retries=0,
                        )
                        self._model=model
                        self._system_template_path=get_base_template_env().get_template("human_prompt.jinja")
                        self._chain_of_thought_template_path=chain_of_thought_template_path
                        self._debug=debug
                        human_first_call = False
                        print("You're using human mode!\n\nAre you a human of adequate general intelligence?\nConsider volunteering your brainpower by answering user queries:\nhttps://discord.gg/YqDn6Dta7t\n")
                        break
                    else:
                        human_first_call = False
                        break

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
