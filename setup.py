#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    nob visual

"""

from glob import glob
from os.path import basename
#from os.path import dirname
#from os.path import join
from os.path import splitext
from setuptools import find_packages, setup

NAME = "nobvisual"
VERSION = "0.0.0a0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


with open("README.md", "r") as fin:
    readme = fin.read()

setup(
    name=NAME,
    version=VERSION,
    description="visialization of nested objets",
    author_email="coop@cerfacs.fr",
    url="",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["nested objects"],
     classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "setuptools",
        "yaml",
        "tkinter",
        "circlify"
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "nobvisual = nobvisual.cli:main_cli",
        ]
    },
)
