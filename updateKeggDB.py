#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Retrieves the taxonomy file and updates organisms that were not present.

Retrieves the taxonomy file listing all organisms and updates the gene ID to
KO mapping files via the KEGG REST API for all organisms specified in the
taxonomy file that were not already present. Modules are also updated.
Files are saved as text files within a subdirectory. Existing files will be
overwritten.

Usage: updateKeggDB.py
"""
from config import *
import urllib
import sys
import buildKeggDB
import buildKeggModuleList


def downloadGeneKO(organism):
    """
    Function to download the gene ID to KO mapping file for an organism via
    KEGG REST API.

    Input: string (organism code)
    Output: saved text file
    """
    try:
        with open(KEGGDIRNAME + '/' + organism + '.txt', 'r'):
            pass
    except:
        urllib.urlretrieve(KOURL + organism,
                           KEGGDIRNAME + '/' + organism + '.txt')


# Main
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[2] == '-h':
        sys.exit(__doc__)
    buildKeggModuleList.buildModuleList()
    buildKeggDB.buildDir(KEGGDIRNAME)
    buildKeggDB.downloadTaxonomy()
    # Download mapping files for all organisms in the list
    for organism in buildKeggDB.buildOrgCodes(ORGANISMGROUP):
        downloadGeneKO(organism)
