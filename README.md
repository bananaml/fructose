<img width="326" alt="Group 311 (2)" src="https://github.com/bananaml/fructose/assets/44653944/8162425c-a485-460f-b816-bcc6be5d2cef">


# LLM calls as strongly-typed functions

Fructose is a python package to create a dependable, strongly-typed interface around an LLM call.

Just slap the `@ai()` decorator on a type-annotated function and call it as you would a function. It's lightweight, syntactic sugar.

``` python
from fructose import Fructose
ai = Fructose()

@ai()
def describe(animals: list[str]) -> str:
  """
  Given a list of animals, use one word that'd describe them all.
  """
  ...g

description = describe(["dog", "cat", "parrot", "goldfish"])
print(description) # -> "pets" type: str
```
The `@ai()` decorator introspects the function and builds a prompt to an LLM to perform the task whenever the function is invoked.

Fructose supports:
- args, kwargs, and return types
- primative types `str` `bool` `int` `float`
- compound types `list` `dict` `tuple` `Enum` `Optional`
- complex datatypes `@dataclass`
- nested types
- custom prompt templates
- local function calling

# 
## Installation
``` bash
pip3 install fructose
```

It currently executes the prompt with OpenAI, so you'll need to use your own OpenAI API Key
``` bash
export OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz
```

# Features

## Complex DataTypes

``` python
from fructose import Fructose
from dataclasses import dataclass

ai = Fructose()

@dataclass
class Person:
    name: str
    hobbies: str
    dislikes: str
    obscure_inclinations: str
    age: int
    height: float
    is_human: bool

@ai()
def generate_fake_person_data() -> Person:
  """
    Generate fake data for a cliche aspiring author
  """
  ...

person = generate_fake_person_data()
print(person)
```

## Local Function Calling

Fructose `ai()` functions can choose to call local Python functions. Yes, even other `@ai()` functions.

Pass the functions into the decorator with the `uses` argument: `@ai(uses = [func_1, func_2])`

For example, here's a fructose function fetching HackerNews comments using a local function and the `requests` library:

``` python
from fructose import Fructose
import requests
from dataclasses import dataclass

ai = Fructose()

def get(uri: str) -> str:
    """
    GET request to a URI
    """
    return requests.get(uri).text

@dataclass
class Comment:
    username: str
    comment: str

@ai(uses=[get], debug=True)
def get_comments(uri: str) -> list[Comment]:
    """
    Gets all base comments from a hacker news post
    """
    ...
    

result = get_comments("https://news.ycombinator.com/item?id=22963649")

for comment in result:
    print(f"🧑 {comment.username}: \n💬 {comment.comment}\n")
```

Local function calling currently requires:
- type annotations on the function
- docstring on the function
- sane variable names for arguments
  
And supports arguments of basic types:
- `str` `bool` `int` `float` and `list`

# Config

Most config may be set at the decorator level:
```python
ai = Fructose(*args, **kwargs)
```
or at the function level
```python
@ai(*args, **kwargs)
```

## Model type
Select your OpenAI model with the `model` keyword. Defaults to `gpt-4-turbo-preview`
```python
ai = Fructose(model = "gpt-3.5-turbo")
```

## Prompting
Fructose has a lightweight prompt wrapper that "just works" in most cases, but you're free to modify it using the below Flavors and Templates features.
Note: we're not satisfied with this specific API, so feel free to give suggestions for alternatives.

### Flavors
Flavors are optional flags to change the behavior of the prompt.
- `random`: adds a random seed into the system prompt, to add a bit more variability
- `chain_of_thought`: splits calls into two steps: chain of thought for reasoning, then the structured generation.

decorator level:
```python
ai = Fructose(["random", "chain_of_thought"])
```

or function level:
```python
@ai(flavors=["random", "chain_of_thought"])
def my_func():
    # ...
```

### Custom System Prompt Templates

You're free to bring your own prompt template, using the Jinja templating language.

To use a custom template on a function level, use the `system_template_path` argument in the `@ai()` decorator, with a relative path to your Jinja template file:

```python
@ai(system_template_path="relative/path/to/my_template.jinja")
def my_func():
    # ...
```

You can also set this on the decorator level, to make it default for all decorated functions.

The template must include the following variables:
-  `func_doc_string`: the docstring from the decorated function
-  `return_type_string`: the string-representation of the function's return types

For reference, [find the default template here](https://github.com/bananaml/fructose/blob/main/src/fructose/templates/default_prompt.jinja)

### Custom Chain Of Thought Prompt Templates

In the case of the `chain_of_thought` flavor being used, fructose will first run a chain-of-thought call, using a special system prompt. 

Customize it on the function level with the `chain_of_thought_template_path` argument in the `@ai()` decorator.

```python
@ai(
    flavors = ["chain_of_thought"], 
    chain_of_thought_template_path="relative/path/to/my_template.jinja"
)
def my_func():
    # ...
```

You can also set this on the decorator level, to make it default for all decorated functions.

For reference, [find the default chain-of-thought template here](https://github.com/bananaml/fructose/blob/main/src/fructose/templates/chain_of_thought_prompt.jinja)

---

## Stability

We are in v0, meaning the API is unstable version-to-version. Pin your versions to ensure new builds don't break!
Also note... since LLM generations are nondeterminsitic, the calls may break too!

## Use Cases

### Gaming

Getting creative but strongly typed responses from LLMs is particularly useful in game dev scenarios.

Here's a prototype of an alien creature merging/breeding game: https://twitter.com/entreprenik/status/1758948061202809066

![fructose in game dev](https://pbs.twimg.com/media/GGjpueBa4AAEFP0?format=jpg&name=4096x4096 "fructose in gamedev")

## Developing and Contributing

From the root of this repo:

Create a virtual env
``` bash
python3 -m venv venv
. ./venv/bin/activate
```

Install fructose into your pip environment with:
``` bash
pip3 install -e .
```
This installs the fructose package in editable mode. All imports of fructose will run the fructose source at `./src/fructose` directly.

Under /examples you'll find different usage examples. And run them like so:
``` bash
python3 examples/fake_data.py
```

Run tests with:
``` bash
python3 -m pytest
```
