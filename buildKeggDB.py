#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Retrieves the taxonomy file listing all organisms and the gene ID to KO mapping
files via the KEGG REST API for all organisms specified in the taxonomy file.
Modules will also be downloaded.
Files are saved as text files within a subdirectory. Existing files will be
overwritten.

Usage: buildKeggDB.py
"""
from config import *
import urllib
import os
import errno
import sys
import buildKeggModuleList


def buildDir(dirname):
    """
    Prepare directory. Create directory if it does not exist.
    """
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dirname):
            raise


def downloadTaxonomy():
    """
    Get taxonomy file with all organism codes from KEGG.
    """
    urllib.urlretrieve(TAXURL, KEGGDIRNAME + '/taxonomy.txt')


def buildOrgCodes(groups):
    """
    Save all organism codes in a list.

    Input: List of strings defning the groups for which taxonomy information
    will be downloaded (Prokaryotes, Eukaryotes)
    Output: List of organism codes
    """
    ORG_CODES = []
    TAXONOMY = []
    with open(KEGGDIRNAME + '/taxonomy.txt', 'r') as f:
        TAXONOMY = f.readlines()
    for line in TAXONOMY:
        assert len(line) > 0
        # get only those organisms from groups that are specified (Prokaryotes,
        # and/or Eukaryotes)
        if line.split('\t')[3].split(';')[0] in groups:
            # append the organism code to the list of all organisms of interest
            ORG_CODES.append(line.split('\t')[1])
    return ORG_CODES


def downloadGeneKO(organism):
    """
    Function to download the gene ID to KO mapping file for an organism via
    KEGG REST API.

    Input: string (organism code)
    Output: saved text file
    """
    urllib.urlretrieve(KOURL + organism, KEGGDIRNAME + '/' + organism + '.txt')


# Main
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        sys.exit(__doc__)
    buildDir(KEGGDIRNAME)
    # Download taxonomy file
    downloadTaxonomy()
    # Download mapping files for all organisms in the list
    for organism in buildOrgCodes(ORGANISMGROUP):
        downloadGeneKO(organism)
    buildKeggModuleList.buildModuleList()
