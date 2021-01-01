#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    nob visual

"""
import os.path as path
from glob import glob
from os.path import basename
#from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import find_packages, setup


# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

setup(
    name= "nobvisual",
    version=version,
    description="visualization of nested objets",
    author_email="coop@cerfacs.fr",
    url="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["nested objects"],
     classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "setuptools",
        "PyYAML",
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
