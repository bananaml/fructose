import click
from . import utils
import shutil, errno
import sys
import os

@click.group()
@click.version_option()
def cli():
    '''
A package for strongly-typed LLM function calling
    '''
    pass

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, file_okay=False), nargs=-1)
def templates(path):
    '''
Copy prompt templates for customization; default: project root.
    '''
    target_path = utils.get_target_dir(path)

    pkgdir = sys.modules['fructose'].__path__[0]
    fullpath = os.path.join(pkgdir, "templates")

    # copy templates/ directory to the target
    # try:
    shutil.copytree(fullpath, target_path, dirs_exist_ok=True)
    # except OSError as exc: # python >2.5
    #     if exc.errno in (errno.ENOTDIR, errno.EINVAL):
    #         shutil.copy(fullpath, target_path)
    #     else: raise

cli.add_command(templates)
