# The AI decorator
import functools
import os
from .type_parser import validate_return_type, type_to_string
from openai import OpenAI
import inspect
import json

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

def send(uses = [], debug = False):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            return_type = inspect.signature(func).return_annotation
            doc_string = inspect.getdoc(func)

            # Get function parameters
            params = inspect.signature(func).parameters
            arguments = dict()

            # Map *args to parameters
            for (param_name, param), arg in zip(params.items(), args):
                arguments[param_name] = arg
                
            # Update args_values with **kwargs which maps directly by name
            arguments.update(kwargs)

            # Handling default values for missing arguments
            for param_name, param in params.items():
                if param_name not in arguments and param.default is not inspect.Parameter.empty:
                    arguments[param_name] = param.default
            
            # TODO if filled args and kwargs is empty, don't include it in the prompt
            rendered_prompt = f"Args: {arguments}, Kwargs: {kwargs}"
            rendered_system = get_system_prompt(doc_string, return_type)

            if debug:
                print("------")
                print("Function name:", func.__name__)
                print("Params and args:", arguments)
                print("System:", rendered_system)
                print("Prompt:", rendered_prompt)
                print("------")

            str_out = call_llm(rendered_system, rendered_prompt)

            if debug:
                print(str_out) 

            return json.loads(str_out)["the_actual_response_you_were_asked_for"]
        return wrapper
    return decorator


def call_llm(rendered_system, rendered_prompt):
    system_suffix = "Answer using JSON using this format: {\"answer_format\": <what should the answer look like? \"single word\", \"list of words\", \"float\", etc>, \"reasoning\": <your reasoning>, \"answer_prep\": <how you're preparing the answer>, , \"answer_examples\": <examples>, \"the_actual_response_you_were_asked_for\": <your final answer>}"
    
    messages = [
            {
                "role": "system",
                "content": (rendered_system + " " + system_suffix).strip()
            },
            {
                "role": "user",
                "content": rendered_prompt
            }
        ]

    chat_completion = client.chat.completions.create(
            # model="gpt-3.5-turbo-1106",
            model="gpt-4-turbo-preview",
            response_format={
                "type":"json_object",
            },
            messages=messages,
            # max_tokens=500,
        )
    return chat_completion.choices[0].message.content


def get_system_prompt(func_docstring: str, return_type: str) -> str:
    return f"""
First figure out what steps you need to take to solve the problem defined by the following: \"{func_docstring}. The return type should be {return_type}\"
        
Then work through the problem. You can write code or pseudocode if necessary.

You may be given a set of arguments to work with.

Be concise and clear in your response.

Take a deep breath and work through it step by step.

Keep track of what was originally asked of you and make sure to actually answer correctly.

If you don't know, try anyway. Believe in yourself.
    """.strip()

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
