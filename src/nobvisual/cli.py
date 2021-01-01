""" command line of nob visualizee"""

import click
import nobvisual as nobv

# not to bu used aside of the CLI
__all__ = []

@click.group()
def main_cli():
    """---------------    NOB VISUAL  --------------------

You are now using the Command line interface of Nob Visual
a Python3 helper to explore Nested Objects, created at CERFACS (https://cerfacs.fr).

This package is mean to be used as a dependency of other packages,
to provide a tkinker canvas rendering the nested structure of nesteds objects.

This is a python package currently installed in your python environement.
"""
    pass

@click.command()
def tree():
    """Show current wkdir visually. 

    """
    nobv.visual_tree()

main_cli.add_command(tree)

@click.command()
@click.argument('filename', nargs=1)
def treefile(filename):
    """Show the content of a serialization file. 
    
    supports JSON, YAML, NML
    """
    nobv.visual_treefile(filename)

main_cli.add_command(treefile)

@click.command()
@click.argument('file_left', nargs=1)
@click.argument('file_right', nargs=1)
def cmpfile(file_left, file_right):
    """Compare the content of two serialization files. 
    
    supports JSON, YAML, NML
    """
    nobv.visual_comparefile(file_left, file_right)

main_cli.add_command(cmpfile)