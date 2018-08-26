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
from pathlib import Path

from .texts import *

# add correct version number here
__version__ = "0.4"

PROGRAMNAME = "PipApp"
VERSION = __version__
COPYRIGHT = "(C) 2016 Sami Salkosuo"
LICENSE = "Licensed under The MIT License."
DESCRIPTION = "Create files and directories for pip-dist enabled Python apps."
CONFIG_FILE = ".pipapp_defaults"


def parse_command_line_args():
    """parse command line args"""
    parser = argparse.ArgumentParser(description='PipApp. {}'.format(DESCRIPTION))
    parser.add_argument(
        '-d', '--dir',
        metavar='DIR',
        help='Root directory where to create new project files and dirs. Default is current directory.'
    )
    parser.add_argument(
        '-v,', '--version',
        action='version',
        version='{} v{}'.format(PROGRAMNAME, VERSION)
    )
    parser.add_argument(
        "project_name",
        metavar='PROJECTNAME',
        help="Name of the generated Project. Has to be a valid Python identifier."
    )
    return parser.parse_args()


def read_config():
    config_file = Path("~").expanduser() / CONFIG_FILE
    config = configparser.ConfigParser()

    if not config_file.exists():
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
        with open(str(config_file), 'w') as open_config_file:
            config.write(open_config_file)

    # read configuration
    config.read(str(config_file))

    return config["DEFAULT"]


def create_file(file_name, file_contents, directory: Path):
    file_path = directory / file_name
    print("Generating {}… ".format(str(file_path)), end="")

    with open(str(file_path), "w") as f:
        if isinstance(file_contents, list):
            for line in file_contents:
                print(line, file=f)
        else:
            print(file_contents, file=f, end="")
    print("Done.")


def create_directory(directory_name: Path):
    if not directory_name.exists():
        directory_name.mkdir(parents=True)


def main():

    args = parse_command_line_args()

    project_name = args.project_name
    base_directory = Path(".") / project_name
    if args.dir:
        base_directory = Path(args.dir).expanduser() / args.project_name
    create_directory(base_directory)

    print("Generating files for project {} in directory {}...".format(project_name, base_directory))

    config = read_config()

    # file: README.rst
    create_file("README.rst", get_readme_txt(project_name), base_directory)

    # file: CHANGES
    current_date = datetime.date.today().strftime("%d.%m.%Y")
    changes = ["Version 0.0.1 ({})".format(current_date), "", "- Initial version."]
    create_file("CHANGES", changes, base_directory)

    # file: LICENSE
    license_text = get_license_txt(config['author'])
    create_file("LICENSE", license_text, base_directory)
    
    # file: setup.cfg
    create_file("setup.cfg", get_setup_cfg_txt(), base_directory)

    # file: PROJECTNAME-runner.py
    create_file("{}-runner.py".format(project_name), get_runner_txt(project_name), base_directory)

    # file: setup.py
    create_file("setup.py", get_setup_py(project_name, config), base_directory)

    # file: MANIFEST.in
    create_file("MANIFEST.in", get_manifest_in(project_name), base_directory)

    # create dir: PROJECTNAME
    src_dir = base_directory / project_name
    print("Creating dir: {}… ".format(src_dir), end="")
    create_directory(src_dir)
    print("Done.")

    # file: PROJECTNAME/PROJECTNAME.py
    create_file("{}.py".format(project_name), get_main_source(project_name, license_text, config), src_dir)
    
    # file: PROJECTNAME/__init__.py
    create_file("__init__.py", get_init_py(project_name), src_dir)

    # file: PROJECTNAME/__main__.py
    create_file("__main__.py", get_main_py(project_name), src_dir)


if __name__ == "__main__": 
    main()
