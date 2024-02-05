# The AI decorator
import functools
import os
import json
from .type_parser import validate_return_type, type_to_string
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

class AIResponseParseError(Exception):
    pass

def _call_llm(rendered_system, rendered_prompt):
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
            model="gpt-4-turbo-preview",
            messages=messages
        )
    return chat_completion.choices[0].message.content

def _parse_return(return_type, string):
    json_result = string.split("# Result\n")[-1].strip()
    # parse out the markdown
    json_result = "\n".join(json_result.split("\n")[1:-1])
    print(json_result)

    try:
        parsed_result = json.loads(json_result)
        result = parsed_result["result"]
    except json.JSONDecodeError as e:
        raise AIResponseParseError("Invalid response from LLM")
    except KeyError as e:
        raise AIResponseParseError("Invalid response from LLM")

    if result != return_type(result):
        raise ValueError("Invalid response from LLM")

    return result

def AI(uses = [], debug = False):
    # quick and dirty print function that only prints if debug is True
    def _print(*args, **kwargs):
        if debug:
            print(*args, **kwargs)

    def decorator(func):
        # annotations are arg1, arg2, ..., return
        arg_repr = {}
        for arg in func.__annotations__:
            if arg != "return":
                arg_repr[arg] = type_to_string(func.__annotations__[arg])

        return_type = func.__annotations__.get("return")

        validate_return_type(func.__name__, func.__annotations__.get("return"))

        return_repr = type_to_string(return_type)

        # naive attempt to render the system prompt, we'll need to make this much nicer
        rendered_system = f""""
{func.__doc__}

You'll receive the following arguments:
{arg_repr}

Your response must be of the following format:
# Chain of Thought
< use this section as a scratch pad to think out loud about what has happened and what might be an interesting and realistic thing to have happen next >
# Result
< you response must be JSON of the following format:
```json
{{
    "result": {return_repr}
}}
```>
""".strip()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _print("---- Calling function ----")
            # we want a string representation of the arguments and kwargs, so we can pass them to the AI
            rendered_prompt = f"Args: {args}, Kwargs: {kwargs}"
            _print("Prompt:\t\t", rendered_prompt)

            str_out = _call_llm(rendered_system, rendered_prompt)
            _print("Response:\t", str_out)

            # attempt to parse the response into the expected type
            res = _parse_return(return_type, str_out)

            _print("Parsed:\t\t", res)
            _print()
            return res
        
        return wrapper
    return decorator
