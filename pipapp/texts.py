# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2016 Sami Salkosuo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime


def getLicenseTxt(author):
    license="""The MIT License (MIT)

Copyright (c) %s %s

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""" % (datetime.date.today().strftime("%Y"),author)
    
    return license


def getReadmeTxt(projectName="PROJECTNAME"):
    readme="""%s
======

Project description

Requirements
------------

Python 3.

Install
-------

Install latest version: **pip install %s**.

Usage
-----

Execute *%s*.


About
-----

""" % (projectName,projectName,projectName)

    return readme


def getSetupCfgTxt():
    text=["[bdist_wheel]","universal = 0"]
    return text


def getRunnerTxt(projectName):
    text='''#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convenience wrapper for running %s directly from source tree."""


from %s.%s import main


if __name__ == '__main__':
    main()
''' % (projectName,projectName,projectName)

    return text


def getManifestIn(projectname):
    txt='''# Include the license file
include LICENSE 
'''
    return txt

def getSetupPy(projectName,config):

    
    txt='''# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup, find_packages

projectName="{pName:s}"
scriptFile="%s/%s.py" % (projectName,projectName)
description="Setuptools setup.py for {pName:s}."


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
    #add required packages to install_requires list
    #install_requires=["package","package2"]
    entry_points = {{
        "console_scripts": ['%s = %s.%s:main' % (projectName,projectName,projectName)]
        }},
    version = version,
    description = description,
    long_description = long_descr,
    author = "{author:s}",
    author_email = "{author_email:s}",
    url = "{url:s}",
    license='{license:s}',
#list of classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers={classifiers:s},
    )
'''.format(pName=projectName,author=config['author'],author_email=config['author_email'],url=config['url'],license=config['license'],classifiers=str(config['classifiers']).replace(",",",\n"))

    return txt


def getInitPy(projectName):
    #empty __init__.py is enough
    txt=""
    return txt  


def getMainPy(projectName):
    txt='''# -*- coding: utf-8 -*-
 
"""{pName:s}.__main__: executed when {pName:s} directory is called as script."""
 
from .{pName:s} import main
main()

'''.format(pName=projectName)


    return txt  

def getMainSource(projectName,license,config):
    txt='''#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
    for line in license.split("\n"):
        txt="%s# %s\n" % (txt,line)



    txt=txt+'''
#add correct version number here
__version__ = "0.0.1"


PROGRAMNAME="{pName:s}"
VERSION=__version__
COPYRIGHT="(C) {currentYear:s} {author:s}"


def main():
    #program logic here
    print("TODO: the application")
    pass

if __name__ == "__main__": 
    main()

'''.format(pName=projectName,currentYear=datetime.date.today().strftime("%Y"),author=config['author'])




    return txt