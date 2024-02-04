# The AI decorator
import functools
import os
from .type_parser import validate_return_type
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

def call_llm(rendered_system, rendered_prompt):
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
    chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    return chat_completion.choices[0].message.content

def parse_return(return_types, string):
    res = None
    
    if return_types == int:
        res = int(string)
    
    elif return_types == float:
        res = float(string)
    
    elif return_types == str:
        res = string
        # llms sometimes return the string with surrounding quotes, so we'll strip them
        if res[0] == '"' and res[-1] == '"':
            res = res[1:-1]
        if res[0] == "'" and res[-1] == "'":
            res = res[1:-1]
    
    elif return_types == bool:
        # llms sometimes return unexpected capitalization on booleans
        if string.lower() == "true":
            res = True
        elif string.lower() == "false":
            res = False
        else:
            raise ValueError("Invalid boolean value")
    
    else:
        raise NotImplementedError("We don't support this return type yet")
    return res

def AI(uses = [], debug = False):
    # quick and dirty print function that only prints if debug is True
    def _print(*args, **kwargs):
        if debug:
            print(*args, **kwargs)

    def introspect(func):
        # introspect the function at definition time to get the type hints
        func_name = func.__name__
        func_signature = func.__annotations__
        func_docstring = func.__doc__
        
        # annotations are arg1, arg2, ..., return
        arg_types = {}
        for arg in func_signature:
            if arg != "return":
                arg_types[arg] = func_signature[arg]

        validate_return_type(func_signature.get("return"))
        return_types = func_signature.get("return") # TODO: python only allows one return type, but we should support Tuple and split it into a list

        _print("---- Decorating function ----")
        _print("Name:\t\t", func_name)
        _print("Arguments:")
        for arg in arg_types:
            _print(f"\t\t {arg}:\t{arg_types[arg]}")
        _print("Returns:")
        _print(f"\t\t {return_types}")
        _print("Docstring:\t", func_docstring)

        # nieve attempt to render the system prompt, we'll need to make this much nicer
        rendered_system = f""""
You're a python emulator which will perform the following function:
{func_docstring}

You'll be given these arguments:
{repr(arg_types)}

You must reply with a value of type:
{repr(return_types)}

Include no extra words in your response, and be as concise as possible.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _print("---- Calling function ----")
            # we want a string representation of the arguments and kwargs, so we can pass them to the AI
            rendered_prompt = f"Args: {args}, Kwargs: {kwargs}"
            _print("Prompt:\t\t", rendered_prompt)

            str_out = call_llm(rendered_system, rendered_prompt)
            _print("Response:\t", str_out)

            # attempt to parse the response into the expected type
            res = parse_return(return_types, str_out)

            _print("Parsed:\t\t", res)
            _print()
            return res
        
        return wrapper
    return introspect