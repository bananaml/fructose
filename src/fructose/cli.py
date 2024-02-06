import click
import openai
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
import os
import json

@click.group()
@click.version_option()
def cli():
    pass


@click.command()
def cook():
    click.echo("Cooking up some code")

cli.add_command(cook)

if __name__ == "__main__":
    cli()
