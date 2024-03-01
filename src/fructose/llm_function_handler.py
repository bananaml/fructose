
import inspect
import json
import os
from typing import Any, Callable, Type, TypeVar, get_type_hints

import openai
import jinja2
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionToolMessageParam, ChatCompletionUserMessageParam
from . import function_helpers, type_parser, types


T = TypeVar('T')

def _validate_return_type_for_function(func_name, return_type):
    """
    Validates that the return type is supported by Fructose.
    """
    if return_type is inspect.Signature.empty:
        raise type_parser.EmptyReturnException(f"Return type for {func_name} is Empty. Please add a return type with this notation: def {func_name}(...) -> your_return_type:")

    if not type_parser.is_supported_return_type(return_type):
        raise NotImplementedError("Fructose does not support return type " + type_parser.type_to_string(return_type) + " yet. Please use int, str, float, bool, or generic types.")

def _parse_llm_result(result: str, return_type: Type[T]) -> T:
    json_result = json.loads(result)
    res = json_result['final_response']

    return type_parser.parse_json_to_type(res, return_type) 

class LLMFunctionHandler():
    def __init__(
        self,
        client: openai.Client,
        model: str,
        func: Callable[..., Any],
        uses: list[Callable[..., Any]],
        flavors: list[types.FructoseFlavor],
        system_template: jinja2.Template,
        chain_of_thought_template: jinja2.Template,
        debug: bool
    ):
        self._client = client
        self._model = model
        self._func = func
        self._uses = uses
        self._uses_lookup = {func.__name__: func for func in uses} if uses else {}
        self._flavors = flavors
        self._debug = debug
        self._system_template = system_template
        self._chain_of_thought_template = chain_of_thought_template
        self._system_message = None
        self._chain_of_thought_message = None
        self._return_annotation = None

        # if the return annotation is a string, then it's a forward reference and we can't validate it
        return_annotation = inspect.signature(func).return_annotation
        if not isinstance(return_annotation, str):
            _validate_return_type_for_function(func.__name__, return_annotation)
            
        
    def _prepare(self):
        type_hints = get_type_hints(self._func)
        self._return_annotation = type_hints.get('return', inspect.Signature.empty)
        _validate_return_type_for_function(self._func.__name__, self._return_annotation)

        return_type_str = type_parser.type_to_string(self._return_annotation)
    
        self._system_message = self._system_template.render(
            func_doc_string=self._func.__doc__,
            return_type_string=return_type_str
        ).strip()

        if 'random' in self._flavors:
            self._system_message += "\n\nRandom seed: " + str(os.urandom(16)) + "\n\n"

        self._chain_of_thought_message = self._chain_of_thought_template.render(
            func_doc_string=self._func.__doc__,
            return_type_string=return_type_str,
            available_tools_string=str(self._tools)
        ).strip()

    @property
    def _tools(self):
        if self._uses == None:
            return None
        return [
            function_helpers.convert_function_to_openai_function(func)
            for func in self._uses
        ]

    def _call_chain_of_thought(self, messages):
        assert self._chain_of_thought_message is not None

        # swap out the system message
        new_system_message = ChatCompletionSystemMessageParam(
            role="system",
            content=self._chain_of_thought_message
        )
        messages = [new_system_message, *messages[1:]]

        # filter out tool messages from end of messages
        last_non_tool_message = -1
        for i, message in enumerate(messages):
            if message['role'] != "assistant" or 'tool_calls' not in message:
                last_non_tool_message = i
        messages = messages[:last_non_tool_message + 1]

        chat_completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
        )

        message = chat_completion.choices[0].message

        return message.content


    # TODO this function is way too long
    def _call_llm(self, messages):
        if self._debug:
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

        perform_cot = {
            "type": "function",
            "function": {
                "name": "perform_chain_of_thought",
                "description": "Call this to think about the problem before trying to solve. Generally it's a good idea to call this before deciding what tools to use or before returning a final answer",
                "parameters": {}
            }
        }
        tool_extension = []
        if "chain_of_thought" in self._flavors:
            tool_extension.append(perform_cot)

        # extend tools with chain of thought
        tools = self._tools
        extended_tools = None
        if tools != None or tool_extension:
            extended_tools = [*(tools or []), *tool_extension]


        if self._debug:
            # print tools in yellow
            print(f"\033[91mTools: {extended_tools}\033[0m")

        chat_completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            tools=extended_tools,
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
            if self._debug:
                print(f"\033[91mTool Calls: {tool_calls}\033[0m")
            for tool_call in tool_calls:
                name = tool_call.function.name
                if name == perform_cot['function']['name']:
                    result = self._call_chain_of_thought(messages)
                else:
                    result = self._uses_lookup[name](**json.loads(tool_call.function.arguments))

                tool_message = ChatCompletionToolMessageParam(
                    role="tool",
                    content=json.dumps(result),
                    tool_call_id=tool_call.id,
                )
                messages = [*messages, tool_message]

            return self._call_llm(messages)

        if self._debug:
            print(result)


        if result is None:
            raise Exception("OpenAI chat completion failed")

        return result

    def __call__(self, *args, **kwargs):
        if self._system_message is None:
            self._prepare()
        labeled_arguments = function_helpers.collect_arguments(self._func, args, kwargs)
        rendered_prompt = f"{labeled_arguments}"

        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=self._system_message
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=rendered_prompt
            )
        ]

        raw_result = self._call_llm(messages)

        result = _parse_llm_result(raw_result, self._return_annotation)

        return result

