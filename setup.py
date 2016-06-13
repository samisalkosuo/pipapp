# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup, find_packages

projectName="pipapp"
scriptFile="%s/%s.py" % (projectName,projectName)
description="Create basic files and directories for pip-dist enabled Python apps."


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open(scriptFile).read(),
    re.M
    ).group(1)
 
 
with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = projectName,
    packages = find_packages(),
    entry_points = {
        "console_scripts": ['%s = %s.%s:main' % (projectName,projectName,projectName)]
        },
    version = version,
    description = description,
    long_description = long_descr,
    author = "Sami Salkosuo",
    author_email = "dev@rnd-dev.com",
    url = "https://github.com/samisalkosuo/pipapp",
    license='MIT',
#list of classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Topic :: Utilities"
    ],
    )