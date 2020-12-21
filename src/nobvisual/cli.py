""" command line of nobvisualizee"""

import click


import nobvisual as nobv


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

def treec():
    """Show current wkdir visually. 

    """
    nobv.visual_tree()

main_cli.add_command(treec)

