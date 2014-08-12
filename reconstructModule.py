#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Extract modules from KEGG Mapper Reconstruct Module via scraping and summarize
output for subsequent analysis.

Explanation of codes:
0 ... complete
1 ... 1 block missing
2 ... 2 blocks missing
3 ... incomplete
4 ... not present

Usage: reconstructModule.py <KO mapping file>
"""
from config import *
import requests
from bs4 import BeautifulSoup
import re
import os
import errno
import sys
import buildKeggModuleList

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    sys.exit(__doc__)

DATAFILE = sys.argv[1]
# SAMPLE = re.search('(?<=/)\w+(?=\.)', DATAFILE).group()
SAMPLE = os.path.split(DATAFILE)[1]
MODULES = KEGGDIRNAME + '/Modules.txt'


def buildDir(dirname):
    """
    Prepare directory. Create directory if it does not exist.
    """
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dirname):
            raise


def getModules(SAMPLE):
    assert os.path.isfile('mappings/' + SAMPLE), 'KO file missing.'
    MODULE_FILE = 'results/' + SAMPLE + '.Modules.tsv'
    Modules = []
    Results = []
    Samplemodules = []

    try:
        fin = open(MODULES, 'r')
    except IOError:
        buildKeggModuleList.buildModuleList()
        fin = open(MODULES, 'r')
    else:
        Modules = fin.read().splitlines()
        fin.close()

    # Upload sample data to KEGG Mapper and scrape output
    url = 'http://www.genome.jp/kegg-bin/find_module_object'
    files = {'uploadfile': (SAMPLE, open('mappings/' + SAMPLE, 'rb'))}
    other_fields = {'mode': 'complete+ng1+ng2'}
    response = requests.post(url, data=other_fields, files=files)
    content = response.text

    soup = BeautifulSoup(content)

    info = set(['(complete)', '(incomplete)', '(1 block missing)',
                '(2 blocks missing)'])

    for element in soup.find_all('li'):
        line = element.get_text()
        if line.startswith('M'):
            module = line[0:6]
            possible = re.findall('\(.*?\)', line)
            infoMissing = set(possible).intersection(info)
            missing = str(list(infoMissing)[0])[1]
            if missing == 'c':
                missing = 0
            elif missing == 'i':
                missing = 3
            Results.append((module + '\t' + str(missing)))
            Samplemodules.append(module)

    for module in Modules:
        if module not in Samplemodules:
            Results.append((module + '\t' + str(4)))

    Results.sort()

    with open(MODULE_FILE, 'w') as fout:
        fout.write('\n'.join(Results))

# Extract information for all samples
if __name__ == '__main__':
    buildDir(RESULTSDIR)
    getModules(SAMPLE)
