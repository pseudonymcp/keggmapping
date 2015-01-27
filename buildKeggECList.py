#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Retrieve the newest list of KEGG EC entries via KEGG REST API and prepare
it in different formats (...).
Create target directory if it does not exist. Existing files will be
overwritten.

Usage: buildKeggECList.py
"""
from config import *
import urllib
import os
import sys
import errno


def buildECList(ECDIRNAME):
    # Prepare download directory. Create directory if it does not exist.
    try:
        os.makedirs(ECDIRNAME)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(ECDIRNAME):
            raise

    # Download EC files from KEGG and save it.
    urllib.urlretrieve('http://rest.kegg.jp/list/enzyme',
                       ECDIRNAME + '/ECList.txt')

    # Prepare file with modules and names and save it.
    try:
        os.remove(ECDIRNAME + '/ECNames.txt')
    except OSError:
        pass

    with open(ECDIRNAME + '/ECList.txt', 'r') as fin, open(
            ECDIRNAME + '/ECNames.txt', 'a') as fout:
        for line in fin.readlines():
            ec = line.split('\t')[0].split(':')[1]
            name = line.split('\t')[1].split(';')[0].strip()
            fout.write(ec + ': ' + name + '\n')

    # Prepare file with modules and save it.
    try:
        os.remove(ECDIRNAME + '/ECs.txt')
    except OSError:
        pass

    with open(ECDIRNAME + '/ECList.txt', 'r') as fin, open(ECDIRNAME +
                                                           '/ECs.txt',
                                                           'a') as fout:
        for line in fin.readlines():
            ec = line.split('\t')[0].split(':')[1]
            fout.write(ec + '\n')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[2] == '-h':
        sys.exit(__doc__)

    buildECList(ECDIRNAME)
