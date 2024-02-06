from setuptools import setup

setup(
    name='fructose',
    version='0.0.2',
    packages=["fructose"],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'fructose = fructose:cli',
        ],
    },
    install_requires=[
        'openai',
        'click'
    ],
    # Additional metadata about your package
    author='Banana',
    author_email='erik@banana.dev',
    description='A package for strongly-typed LLM function calling',
    url='https://github.com/bananaml/fructose',
)
