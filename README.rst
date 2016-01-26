PipApp
======

PipApp creates directories and files for Pip-distributable Python application.

Inspired by no-nonsense blog post about Python application distribution (https://gehrcke.de/2014/02/distributing-a-python-command-line-application/).

Requirements
------------

Python 3.

Install
-------

Install latest version: **pip install pipapp**.

Usage
-----

Execute 

*pipapp [PROJECTNAME]* 

and basic set of files and directories (as descibed in no-nonsense blog post) are automagically created in ./PROJECTNAME directory. The main source file is PROJECTNAME.py in ./PROJECTNAME/PROJECTNAME directory. PipApp is not used after initial creation of directories and files, so you can go ahead and develop, register with PyPi and upload the application to PyPi. 

If current directory is not good, you can specify directory where to create files and dirs::

	-d DIR, --dir DIR  Root directory where to create new project files and dirs. Default is current directory.

About
-----

PipApp is meant to give quick start to develop pip-distributable Python applications by providing basic set of files and directories. 
Currently basic set is enough and if you need more professional style of working, please see https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/.
