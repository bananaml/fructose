from functools import wraps
import inspect
import json
import os
from typing import Any, Type, TypeVar
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionToolMessageParam
from pathlib import Path
from fructose import type_parser
from . import function_helpers
import openai
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape, StrictUndefined

DEFAULT_MODEL = "gpt-4-turbo-preview"
# DEFAULT_MODEL = "gpt-3.5-turbo"

T = TypeVar('T')

LabeledArguments = dict[str, Any]

def _validate_return_type_for_function(func_name, return_type):
    """
    Validates that the return type is supported by Fructose.
    """
    if return_type is inspect.Signature.empty:
        raise type_parser.EmptyReturnException(f"Return type for {func_name} is Empty. Please add a return type with this notation: def {func_name}(...) -> your_return_type:")

    if not type_parser.is_supported_return_type(return_type):
        raise NotImplementedError("Fructose does not support return type " + type_parser.type_to_string(return_type) + " yet. Please use int, str, float, bool, or generic types.")


class Fructose():
    def __init__(self, client=None, model=DEFAULT_MODEL, template=None, debug=False):
        if client is None:
            client = openai.Client(
                api_key=os.environ['OPENAI_API_KEY']
            )
        self._client = client
        self._model = model
        self._template = template
        self._debug = debug

    def _call_llm(self, messages: list[ChatCompletionMessageParam], tools, uses, debug: bool) -> str:
        if debug:
            for message in messages:
                if message['role'] == "system":
                    # print color: blue
                    print(f"\033[94mSystem: {message['content']}\033[0m")
                elif message['role'] == "user":
                    # print color: green
                    print(f"\033[92mUser: {message['content']}\033[0m")
                elif message['role'] == "assistant" and 'tool_calls' in message:
                    # print color: red
                    print(f"\033[91mTools: {message['tool_calls']}\033[0m")
                else:
                    # purple other
                    print(f"\033[95mOther: {message}\033[0m")

            # print tools in red
            print(f"\033[91mTools: {tools}\033[0m")

        chat_completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            tools=tools,
            response_format={
                "type":"json_object",
            },
        )

        message = chat_completion.choices[0].message
        result = message.content
        tool_calls = message.tool_calls

        if tool_calls:
            messages = [*messages, {
                "role": "assistant",
                "tool_calls": tool_calls,
            }]
            uses_lookup = {use.__name__: use for use in uses}
            if debug:
                print(f"\033[91mTool Calls: {tool_calls}\033[0m")
            for tool_call in tool_calls:
                function = uses_lookup[tool_call.function.name]
                args = json.loads(tool_call.function.arguments)
                result = function(**args)

                tool_message = ChatCompletionToolMessageParam(
                    role="tool",
                    content=json.dumps(result),
                    tool_call_id=tool_call.id,
                )
                messages = [*messages, tool_message]

            return self._call_llm(messages, tools, uses, debug)

        if debug:
            print(result)


        if result is None:
            raise Exception("OpenAI chat completion failed")

        return result

    def _parse_llm_result(self, result: str, return_type: Type[T]) -> T:

        json_result = json.loads(result)
        res = json_result['final_response']

        return type_parser.parse_json_to_type(res, return_type) 

    def _render_prompt(self, labeled_arguments: dict[str, Any]) -> str:
        return f"{labeled_arguments}"


    def __call__(self, uses=None, flavors=None, template=None, debug=False):
        if flavors is None:
            flavors = []
        _flavors = flavors
        _template = template if template is not None else self._template

        tools = None
        if uses is not None:
            tools = [
                function_helpers.convert_function_to_openai_function(func)
                for func in uses
            ]

            if debug:
                print(f"\033[91mTools: {tools}\033[0m")


        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                labeled_arguments = function_helpers.collect_arguments(func, args, kwargs)
                rendered_prompt = self._render_prompt(labeled_arguments)

                messages = [
                    ChatCompletionSystemMessageParam(
                        role="system",
                        content=rendered_system
                    ),
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=rendered_prompt
                    )
                ]
                raw_result = self._call_llm(messages, tools, uses, debug)
                result = self._parse_llm_result(raw_result, inspect.signature(func).return_annotation)

                return result

            def _render_system(func_doc_string: str, return_type_str: str ) -> str:
                if _template is None:
                    # loader=PackageLoader("fructose", "templates")
                    p = Path(__file__).parent / 'templates'
                    loader = FileSystemLoader(p)
                else:
                    loader=FileSystemLoader(searchpath="./")

                jinja_env = Environment(
                    loader=loader,
                    undefined=StrictUndefined
                    # autoescape=select_autoescape()
                )

                default_template = 'chain_of_thought_json.jinja'

                system = jinja_env.get_template(default_template if _template is None else _template)\
                    .render(func_doc_string=func_doc_string, return_type_string=return_type_str)\
                    .strip()
                
                if "random" in _flavors:
                    system += "\n\nRandom seed: " + str(os.urandom(16)) + "\n\n"

                return system
            
            return_annotation = inspect.signature(func).return_annotation
            _validate_return_type_for_function(func.__name__, return_annotation)

            return_type_str = type_parser.type_to_string(return_annotation)

            rendered_system = _render_system(func.__doc__, return_type_str)
            
            return wrapper
        
        return decorator
