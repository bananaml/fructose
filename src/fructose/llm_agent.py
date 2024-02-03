import os
from typing import TypeVar
from openai import OpenAI

from fructose import type_parser

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

class SystemInstructions():
    def __init__(self, instructions):
        self._instructions = instructions

    def render(self, input_format_desc):
        return self._instructions

class BasicPrompt():
    def render(self, input):
        return str(input)

class OpenAIEngine():
    def __init__(self, client):
        self._client = client

    def __call__(self, messages):
        chat_completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return chat_completion.choices[0].message.content

# type var for input format
T = TypeVar('T')
# type var for response format
R = TypeVar('R')

class LLMAgent():
    def __init__(self, 
                 system_template: SystemInstructions, 
                 prompt: BasicPrompt,
                 input_format: T,
                 response_format: R):
        self._system_template = system_template
        self._prompt = prompt
        self._input_format = input_format
        self._response_format = response_format
        self._functions = []
        # TODO blagh this is gross
        self._llm_engine = OpenAIEngine(client)

    def register_function(self, function):
        self._functions.append(function)
        return function

    def __call__(self, input):
        rendered_prompt = self._prompt.render(input)
        # TODO  does python support generics? this would make this easier
        input_format_desc = type_parser.type_to_string(self._input_format)
        rendered_system = self._system_template.render(
            # functions=self._functions,
            input_format_desc=input_format_desc
        )

        messages = [
            {
                "role": "system",
                "content": rendered_system
            },
            {
                "role": "user",
                "content": rendered_prompt
            }
        ]

        response = self._llm_engine(messages)

        # this can raise an exception, we may want to add retry logic here in the future
        # TODO parse here
        # return self._response_format.parse(response)

        return response
