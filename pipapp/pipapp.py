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

#add correct version number here
__version__ = "0.4"

PROGRAMNAME="PipApp"
VERSION=__version__
COPYRIGHT="(C) 2016 Sami Salkosuo"
LICENSE="Licensed under The MIT License."
DESCRIPTION="Create files and directories for pip-dist enabled Python apps."
CONFIG_FILE=".pipapp_defaults"

import argparse
import configparser
import os
import datetime
import sys
from .texts import *

from os.path import expanduser

BASEDIR="."
PROJECTNAME=None
#command line args
args=None

def parseCommandLineArgs():
    #parse command line args
    parser = argparse.ArgumentParser(description='PipApp. %s' % DESCRIPTION)
    parser.add_argument('-d','--dir', nargs=1,metavar='DIR', help='Root directory where to create new project files and dirs. Default is current directory.')
    parser.add_argument('-v,--version', action='version', version="%s v%s" % (PROGRAMNAME, VERSION))
    parser.add_argument("projectname",metavar='PROJECTNAME', nargs=1)
    global args
    args = parser.parse_args()

def readConfig():
    homeDir = expanduser("~")
    configFile="%s/%s" % (homeDir,CONFIG_FILE)
    config = configparser.ConfigParser()

    if os.path.isfile(configFile) == False:
        #create default configrutaion
        cfg={}
        cfg['author']="Your Name"
        cfg['author_email']="Your Email"
        cfg['url']="http://Project.url.here"
        cfg['license']="MIT"
        cfg['classifiers']=["Development Status :: 1 - Planning",
                            "License :: OSI Approved :: MIT License",
                            "Environment :: Console",
                            "Natural Language :: English",
                            "Operating System :: OS Independent",
                            "Programming Language :: Python :: 3.4",
                            "Programming Language :: Python :: 3.5",
                            "Programming Language :: Python :: 3 :: Only"]


        config['DEFAULT'] = cfg
        with open(configFile, 'w') as configfile:
            config.write(configfile)

    #read configurato
    config.read(configFile)

    return config["DEFAULT"]


def createFile(fileName,fileContents,directory):
    print("Generating %s/%s...." % (directory,fileName), end="")
    f=open("%s/%s" % (directory,fileName) ,"w")
    if isinstance(fileContents, (list)):
        for line in fileContents:
            print(line,file=f)
    else:
        print(fileContents,file=f,end="")
    f.close()
    print("Done.")

def createDirectory(directoryName):
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

def main():

    parseCommandLineArgs()

    PROJECTNAME=args.projectname[0]
    global BASEDIR
    BASEDIR=PROJECTNAME
    if args.dir:
        BASEDIR="%s/%s" % (args.dir[0],PROJECTNAME)
    createDirectory(BASEDIR)

    print("Generating files for project %s in dir %s..." % (PROJECTNAME,BASEDIR))

    config=readConfig()

    #file: README.rst
    createFile("README.rst",getReadmeTxt(PROJECTNAME),BASEDIR)

    #file: CHANGES
    currentDate=datetime.date.today().strftime("%d.%m.%Y")
    changes=["Version 0.1 (%s)" % currentDate,"","- Initial version."]
    createFile("CHANGES",changes,BASEDIR)

    #file: LICENSE
    license=getLicenseTxt(config['author'])
    createFile("LICENSE",license,BASEDIR)
    
    #file: setup.cfg
    createFile("setup.cfg",getSetupCfgTxt(),BASEDIR)

    #file: PROJECTNAME-runner.py
    createFile("%s-runner.py" % PROJECTNAME,getRunnerTxt(PROJECTNAME),BASEDIR)

    #file: setup.py
    createFile("setup.py",getSetupPy(PROJECTNAME,config),BASEDIR)

    #file: MANIFEST.in
    createFile("MANIFEST.in",getManifestIn(PROJECTNAME),BASEDIR)

    #create dir: PROJECTNAME
    srcDir=BASEDIR+"/"+PROJECTNAME
    print("Creating dir: %s..." % srcDir, end="")
    createDirectory(srcDir)
    print("Done.")

    #file: PROJECTNAME/PROJECTNAME.py
    createFile("%s.py" % PROJECTNAME,getMainSource(PROJECTNAME,license,config),srcDir)
    
    #file: PROJECTNAME/__init__.py
    createFile("__init__.py" ,getInitPy(PROJECTNAME),srcDir)

    #file: PROJECTNAME/__main__.py
    createFile("__main__.py" ,getMainPy(PROJECTNAME),srcDir)



if __name__ == "__main__": 
    main()
