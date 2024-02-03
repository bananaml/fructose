from setuptools import setup, find_packages

setup(
    name='fructose',p
    version='0.0.1',
    packages=["fructose"],
    package_dir={'fructose': 'src/fructose'},
    install_requires=[
        # List your package's dependencies here, e.g.,
        # 'numpy>=1.18.0',
    ],

    # Additional metadata about your package
    author='Banana',
    author_email='erik@banana.dev',
    description='A package for strongly-typed LLM function calling',
    url='https://github.com/bananaml/fructose',
)
