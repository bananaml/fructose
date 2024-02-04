# The AI decorator
import functools
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

def call(rendered_system, rendered_prompt):
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

def AI(uses = []):
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

        return_types = func_signature.get("return") # TODO: python only allows one return type, but we should support Tuple and split it into a list
        
        print("---- Decorating function ----")
        print("Name:\t\t", func_name)
        print("Arguments:")
        for arg in arg_types:
            print(f"\t\t {arg}:\t{arg_types[arg]}")
        print("Returns:")
        print(f"\t\t {return_types}")
        print("Docstring:\t", func_docstring)

        # nieve attempt to render the system prompt, we'll need to make this much nicer
        rendered_system = f""""
Perform the following function:
{func_docstring}

You'll be given these arguments:
{repr(arg_types)}

You should reply with a value of type:
{repr(return_types)}

Include no extra words in your response, and be as concise as possible.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("---- Calling function ----")
            # we want a string representation of the arguments and kwargs, so we can pass them to the AI
            rendered_prompt = f"Args: {args}, Kwargs: {kwargs}"
            print("Prompt:\t\t", rendered_prompt)

            res = call(rendered_system, rendered_prompt)
            print("Response:\t", res)
            print()
            return res
        
        return wrapper
    return introspect