#!/usr/bin/env python3
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


import argparse
import configparser
import os
from os.path import expanduser

from .texts import *

# add correct version number here
__version__ = "0.4"

PROGRAMNAME = "PipApp"
VERSION = __version__
COPYRIGHT = "(C) 2016 Sami Salkosuo"
LICENSE = "Licensed under The MIT License."
DESCRIPTION = "Create files and directories for pip-dist enabled Python apps."
CONFIG_FILE = ".pipapp_defaults"


BASEDIR = "."
PROJECTNAME = None
# command line args
args = None


def parse_command_line_args():
    """parse command line args"""
    parser = argparse.ArgumentParser(description='PipApp. {}'.format(DESCRIPTION))
    parser.add_argument(
        '-d', '--dir',
        nargs=1,
        metavar='DIR',
        help='Root directory where to create new project files and dirs. Default is current directory.'
    )
    parser.add_argument(
        '-v,', '--version',
        action='version',
        version='{} v{}'.format(PROGRAMNAME, VERSION)
    )
    parser.add_argument(
        "projectname",
        metavar='PROJECTNAME',
        nargs=1
    )
    global args
    args = parser.parse_args()


def read_config():
    home_dir = expanduser("~")
    config_file = "{}/{}".format(home_dir, CONFIG_FILE)
    config = configparser.ConfigParser()

    if not os.path.isfile(config_file):
        # create default configuration
        cfg = {
            'author': "Your Name",
            'author_email': "Your Email",
            'url': "http://Project.url.here", 'license': "MIT",
            'classifiers': [
                   "Development Status :: 1 - Planning",
                   "License :: OSI Approved :: MIT License",
                   "Environment :: Console",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3 :: Only"
               ]
        }

        config['DEFAULT'] = cfg
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    # read configuration
    config.read(config_file)

    return config["DEFAULT"]


def create_file(file_name, file_contents, directory):
    print("Generating {}/{}....".format(directory, file_name), end="")

    with open("{}/{}".format(directory, file_name), "w") as f:
        if isinstance(file_contents, list):
            for line in file_contents:
                print(line, file=f)
        else:
            print(file_contents, file=f, end="")
    print("Done.")


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def main():

    parse_command_line_args()

    PROJECTNAME = args.projectname[0]
    global BASEDIR
    BASEDIR = PROJECTNAME
    if args.dir:
        BASEDIR = "{}/{}".format(args.dir[0], PROJECTNAME)
    create_directory(BASEDIR)

    print("Generating files for project {} in dir {}...".format(PROJECTNAME, BASEDIR))

    config = read_config()

    # file: README.rst
    create_file("README.rst", get_readme_txt(PROJECTNAME), BASEDIR)

    # file: CHANGES
    current_date = datetime.date.today().strftime("%d.%m.%Y")
    changes = ["Version 0.1 ({})".format(current_date), "", "- Initial version."]
    create_file("CHANGES", changes, BASEDIR)

    # file: LICENSE
    license_text = get_license_txt(config['author'])
    create_file("LICENSE", license_text, BASEDIR)
    
    # file: setup.cfg
    create_file("setup.cfg", get_setup_cfg_txt(), BASEDIR)

    # file: PROJECTNAME-runner.py
    create_file("{}-runner.py".format(PROJECTNAME), get_runner_txt(PROJECTNAME), BASEDIR)

    # file: setup.py
    create_file("setup.py", get_setup_py(PROJECTNAME, config), BASEDIR)

    # file: MANIFEST.in
    create_file("MANIFEST.in", get_manifest_in(PROJECTNAME), BASEDIR)

    # create dir: PROJECTNAME
    src_dir=BASEDIR+"/"+PROJECTNAME
    print("Creating dir: {}...".format(src_dir), end="")
    create_directory(src_dir)
    print("Done.")

    # file: PROJECTNAME/PROJECTNAME.py
    create_file("{}.py".format(PROJECTNAME), get_main_source(PROJECTNAME, license_text, config), src_dir)
    
    # file: PROJECTNAME/__init__.py
    create_file("__init__.py", get_init_py(PROJECTNAME), src_dir)

    # file: PROJECTNAME/__main__.py
    create_file("__main__.py", get_main_py(PROJECTNAME), src_dir)


if __name__ == "__main__": 
    main()
