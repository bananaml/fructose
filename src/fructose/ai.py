from functools import wraps
import inspect
import json
import os
import ast
import dataclasses
from typing import Any, Type, TypeVar, get_args
from collections.abc import Container
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from fructose.type_parser import type_to_string, validate_return_type_for_function, describe_dataclass_as_dict, validate_container_type, perform_type_validation
from . import function_helpers
import openai

T = TypeVar('T')

LabeledArguments = dict[str, Any]

class Fructose():
    def __init__(self, client=None, model="gpt-4-turbo-preview"):
        if client is None:
            client = openai.Client(
                api_key=os.environ['OPENAI_API_KEY']
            )
        self._client = client
        self._model = model
        self._flavors = []

    def _call_llm(self, messages: list[ChatCompletionMessageParam], debug: bool) -> str:
        if debug:
             for message in messages:
                if message['role'] == "system":
                    # print color: blue
                    print(f"\033[94mSystem: {message['content']}\033[0m")
                else:
                    # print color: green
                    print(f"\033[92mUser: {message['content']}\033[0m")

        chat_completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            response_format={
                "type":"json_object",
            },
        )

        result = chat_completion.choices[0].message.content
        if debug:
            print(result)


        if result is None:
            raise Exception("OpenAI chat completion failed")

        return result

    def _parse_llm_result(self, result: str, return_type: Type[T]) -> T:

        json_result = json.loads(result)
        res = json_result['final_response']

        # if the return type is a dataclass, we need to convert the result to a dataclass
        if dataclasses.is_dataclass(return_type):
            typed_result = return_type(**res)
        # if the return type is string we don't need to do anything
        elif return_type == str:
            typed_result = res
        # else we use the ast lib to evaluate any string as a valid python expression
        # this is needed e.g when the LLM returns "False" as a string
        else:
            res = ast.literal_eval(str(res))
            typed_result = return_type(res)

        perform_type_validation(typed_result, return_type)

        return typed_result

    def _render_system(self, func_doc_string: str, return_type_str: str ) -> str:
        system = f"""
You are an AI assistant tasked with the following problem:

{func_doc_string.strip()}

The user will provide you with the necessary arguments to solve the problem. Your response should be in the following format: {return_type_str}.

Answer with JSON in this format: 
{{
    \"chain_of_thought\": <use this as a scratch pad to reason over the request>, 
    \"final_response\": <your final answer in the format requested: {return_type_str}>
}}
""".strip()
        
        if "random" in self._flavors:
            system += "\n\nRandom seed: " + str(os.urandom(16)) + "\n\n"

        return system


    def _render_prompt(self, labeled_arguments: dict[str, Any]) -> str:
        return f"{labeled_arguments}"


    def __call__(self, flavors=None, debug=False):
        if flavors is None:
            flavors = []
        self._flavors = flavors

        def decorator(func):
            return_annotation = inspect.signature(func).return_annotation
            validate_return_type_for_function(func.__name__, return_annotation)

            # we want to convert the dataclass to a dict of specific format and then convert it to a string
            if dataclasses.is_dataclass(return_annotation):
                return_annotation = describe_dataclass_as_dict(return_annotation)
                return_type_str = str(return_annotation)
            # all other types should be converted to a string straight away
            else:
                return_type_str = type_to_string(return_annotation)

            rendered_system = self._render_system(func.__doc__, return_type_str)

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
                raw_result = self._call_llm(messages, debug)
                result = self._parse_llm_result(raw_result, inspect.signature(func).return_annotation)

                return result

            return wrapper

        return decorator
