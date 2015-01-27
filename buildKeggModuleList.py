#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Retrieve the newest list of KEGG modules via KEGG REST API and prepare
it in different formats (modules, modules with names, original file).
Create target directory if it does not exist. Existing files will be
overwritten.

Usage: buildKeggModuleList.py
"""
from config import *
import urllib
import os
import sys
import errno


def buildModuleList():
    # Prepare download directory. Create directory if it does not exist.
    try:
        os.makedirs(KEGGDIRNAME)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(KEGGDIRNAME):
            raise

    # Download modules files from KEGG and save it.
    urllib.urlretrieve('http://rest.kegg.jp/list/module',
                       KEGGDIRNAME + '/ModuleList.txt')

    # Prepare file with modules and names and save it.
    try:
        os.remove(KEGGDIRNAME + '/ModulesNames.txt')
    except OSError:
        pass

    with open(KEGGDIRNAME + '/ModuleList.txt', 'r') as fin, open(
            KEGGDIRNAME + '/ModulesNames.txt', 'a') as fout:
        for line in fin.readlines():
            module = line.split('\t')[0].split(':')[1]
            name = line.split('\t')[1]
            fout.write(module + ': ' + name)

    # Prepare file with modules and save it.
    try:
        os.remove(KEGGDIRNAME + '/Modules.txt')
    except OSError:
        pass

    with open(KEGGDIRNAME + '/ModuleList.txt', 'r') as fin, open(KEGGDIRNAME +
                                                                 '/Modules.txt',
                                                                 'a') as fout:
        for line in fin.readlines():
            module = line.split('\t')[0].split(':')[1]
            fout.write(module + '\n')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[2] == '-h':
        sys.exit(__doc__)
    buildModuleList()
