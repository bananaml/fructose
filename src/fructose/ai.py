# The AI decorator
import functools
import os
from .type_parser import validate_return_type, type_to_string
from openai import OpenAI
import json 


client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

def call_llm(rendered_system, rendered_prompt, foo = None):
    system_suffix = "Answer using JSON using this format: {\"reasoning\": <your reasoning>, \"answer\": <your final answer>}" # if foo is None else "use the functions provided."
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
    
    if foo is not None:
        messages.append(
            {
                "role": "assistant",
                "content": foo
            }
        )
        messages.append(
            {
                "role": "user",
                "content": "What is the final answer?"
            }
        )

    print(messages)

    chat_completion = client.chat.completions.create(
            # model="gpt-3.5-turbo-1106",
            model="gpt-4-turbo-preview",
            response_format={
                "type":"json_object",
            },  #if foo is not None else None,
            # seed=42, # possoibly make this dynamic based on prompt
            # temperature=1,
            messages=messages,
            max_tokens=500,
            # tools=[{
            #     "type": "function",
            #     "function": {
            #         "name": "use_avg_length_answer",
            #         "description": "The answer to the user's question",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "res": {
            #                     "type": "number",
            #                     # "items": {
            #                     #     "type": "string",
            #                     # },
            #                     "description": "the average length of the words"
            #                 }
            #             },
            #         },
            #         # "required": ["baz"]
            #     },
            # }, {
            #     "type": "function",
            #     "function": {
            #         "name": "use_theme_answer",
            #         "description": "The answer to the user's question",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "res": {
            #                     "type": "string",
            #                     # "items": {
            #                     #     "type": "string",
            #                     # },
            #                     "description": "the common theme for the given list of words."
            #                 }
            #             },
            #         },
            #         # "required": ["baz"]
            #     },
            # }, {
            #     "type": "function",
            #     "function": {
            #         "name": "random_word",
            #         "description": "The answer to the user's question (the chosen random word)",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "res": {
            #                     "type": "string",
            #                     # "items": {
            #                     #     "type": "string",
            #                     # },
            #                     "description": "the chose random word for the user to guess in a hangman game"
            #                 }
            #             },
            #         },
            #         # "required": ["baz"]
            #     },
            # }] if foo is not None else None,
        )
    # if foo is not None:
        # print(json.loads(chat_completion.choices[0].message.tool_calls[0].function.arguments))

    print(chat_completion.choices[0].message.content)
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

        # todo dict
        # validate_return_type(func_name, func_signature.get("return"))
        return_types = func_signature.get("return") # TODO: python only allows one return type, but we should support Tuple and split it into a list

        _print("---- Decorating function ----")
        _print("Name:\t\t", func_name)
        _print("Arguments:")
        for arg in arg_types:
            _print(f"\t\t {arg}:\t{type_to_string(arg_types[arg])}")
        _print("Returns:")
        _print(f"\t\t {type_to_string(return_types)}")
        _print("Docstring:\t", func_docstring)

        # nieve attempt to render the system prompt, we'll need to make this much nicer
        arg_repr = {}
        for arg in arg_types:
            arg_repr[arg] = type_to_string(arg_types[arg])
        return_repr = type_to_string(return_types)
        example = ""
        rendered_system = f"""
        First figure out what steps you need to take to solve the problem defined by the following: {func_docstring}
        
        Then work through the problem. You can write code or pseudocode if necessary.

        You may be given a set of arguments to work with.

        Be concise and clear in your response.

        Take a deep breath and work through it step by step.

        Keep track of what was originally asked of you and make sure to actually answer correctly.
        """.strip()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _print("---- Calling function ----")
            _print(args)
            filled_args = {}
            for i, arg in enumerate(args):
                filled_args[list(arg_types.keys())[i]] = arg
            filled_args.update(kwargs) # ??
            
            _print(filled_args)
            # we want a string representation of the arguments and kwargs, so we can pass them to the AI
            # if filled args and kwargs is empty, don't include it in the prompt
            rendered_prompt = f"Args: {filled_args}, Kwargs: {kwargs}" # ; Don't actually answer, just plan out the strategy.
            _print("Prompt:\t\t", rendered_system, rendered_prompt)

            # step1 
            str_out = call_llm(rendered_system, rendered_prompt)
            _print("Respons1e:\t", str_out)

            # step2 - use the response to add an assistant message and get the final answer
            # str_out = call_llm(rendered_system, rendered_prompt, str_out)
            # _print("Response2:\t", str_out)

            # attempt to parse the response into the expected type
            # res = parse_return(return_types, str_out)

            # _print("Parsed:\t\t", res)
            _print()
            return res
        
        return wrapper
    return introspect
