from setuptools import setup

setup(
    name='fructose-ai',
    version='0.0.1',
    packages=["fructose"],
    package_dir={'fructose': 'src/fructose'},
    install_requires=[
        'openai',
    ],

    # Additional metadata about your package
    author='Banana',
    author_email='erik@banana.dev',
    description='A package for strongly-typed LLM function calling',
    url='https://github.com/bananaml/fructose',
)
