#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="python_lib",
    version="1.0",
    description="Python library",
    author=["Yue Ma"],
    url="https://github.com/mayueanyou/python_lib",
    packages=find_packages(),
    install_requires=requirements,
    #entry_points={"console_scripts": ["inclearn = inclearn.__main__:main"]},
)