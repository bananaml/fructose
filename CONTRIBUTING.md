# Contributing to Fructose

Fructose is a new package, backed by [Banana](https://banana.dev), and we're still exploring the right abstractions. 

The most helpful you can be to this project is sharing your experience with structured LLM generation, and using `Issues` to discuss potential improvements to the package's design.

## Project goals

The goal of Fructose is to explore the interface between programming languages and LLMs.

The guiding principles of this exploration are:
1. Use the python language as the API. The core of fructose is the @ai decorator and its `uses` argument, all operating on native python functions and native python types. This is intentional; it enables features through composition rather than explicitly adding them through the package.
2. Keep it slim. Avoid config and hidden behavior. Endless layers of abstractions, function arguments, and config do not make a package better.

**Fructose should feel like a language feature, not a package to learn.**
It should be boring.


## Suggestions

**Abstraction design / language design ideas** are interesting if they unlock a more programmable, more python-language interface to LLMs. 

Please suggest them using `Issues`.

We're especially interested in finding a better API for:
- dynamic system prompts. How can users change / modify / metaprogram the prompt at runtime? The `flavors` argument is an attempt at this, but it goes against the design goals of the package because it's a hardcoded behavior. Do we even want that?
- chain of thought, and other common intelligence patterns. How can it be expressed by composing fructose functions together vs needing to hardcode the behavior into the package.
- context and persistence, how do users best carry context for prior calls through to future calls? do we even want that? 

Please include example python code for how you'd prefer the interaction to behave, and explain where the current package design falls short.


**Long tail features:**
Suggestions for additional arguments, functions, LLM providers, internal behaviors, non-python datatypes, etc will likely not be acted on. The core functionality is there and we need to ensure it's the right direction before loading the package with long tail features.

## Bug Reports

Internal can be reported through `Issues`. Please include:
- Your fructose version
- All relevant clientside code
- Logs and exception stack traces

Fixes to these bug reports would be great first-contribution PRs!

## Pull Requests

PRs are great, especially for internal bug fixes, adding examples, and updating documentation.

PRs are expected to pass tests without regression. Please confirm in the PR that you've ran the tests:
```bash
python3 -m pytest --verbose 
```

If you're making any prompting changes, please also run the evals and report the score. It doesn't need to be 100%.
```bash
python3 eval/elderberry_eval.py
```

Very few PRs that change/add to the API without prior design approval will be accepted. Please find a relevant discussion in `Issues` or open one yourself.
