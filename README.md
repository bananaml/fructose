# fructose

### Running LLMs as strongly-typed functions
```
from fructose import AI

@AI()
def get_theme(words: list[str]) -> str:
  """
  This function takes a list of words and returns a theme.
  """

theme = get_theme(["cat", "dog", "bird"])
print(theme) # animals
```

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

Run the demo with
``` bash
python3 demo.py
```