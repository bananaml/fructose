# Fructose: LLM calls as strongly-typed functions

Implement LLM calls as python functions, using the docstring and type signatures to establish the API.
```
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

person = generate_fake_person_data()
print(person)
```
The @ai() decorator introspects the function and builds a prompt to an LLM to perform the task whenever the function is invoked.

It currently executes the prompt with gpt-4, so you'll need to use your own OpenAI API Key
```export OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz```

---

### Stability

We are in v0, meaning the API is unstable version-to-version. Pin your versions to ensure new builds don't break!
Also note... since LLM generations are nondeterminsitic, the calls may break too!

### To develop

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
