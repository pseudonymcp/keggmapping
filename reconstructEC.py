#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Summarize ECs present and absent in a EC annotation file.

Explanation of codes:
0 ... not present
1 ... present

Usage: reconstructEC.py <EC mapping file>
"""
from config import *
import re
import os
import errno
import sys
import buildKeggECList

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    sys.exit(__doc__)

DATAFILE = sys.argv[1]
# SAMPLE = re.search('(?<=/)\w+(?=\.)', DATAFILE).group()
SAMPLE = os.path.split(DATAFILE)[1]
ECS = ECDIRNAME + '/ECs.txt'


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [atoi(c) for c in re.split('(\d+)', text)]


def buildDir(dirname):
    """
    Prepare directory. Create directory if it does not exist.
    """
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dirname):
            raise


def getECs(SAMPLE, ECMAPPINGSDIR, ECRESULTSDIR, ECDIRNAME):
    assert os.path.isfile(ECMAPPINGSDIR + '/' + SAMPLE), 'EC file missing.'
    ECall = []

    try:
        fin = open(ECS, 'r')
    except IOError:
        buildKeggECList.buildECList(ECDIRNAME)
        fin = open(ECS, 'r')
    else:
        ECall = fin.read().splitlines()
        fin.close()

    ECall.sort(key=natural_keys)
    ec_list = []
    Results = []

    with open(ECMAPPINGSDIR + '/' + SAMPLE, 'r') as fin,\
            open(ECRESULTSDIR + '/' + SAMPLE + '.EC.tsv', 'w') as fout:
        for line in fin.readlines():
            ec = line.split('\t')[1].strip()
            ec_list.append(ec)
        ec_list.sort(key=natural_keys)

        for ec in ECall:
            if ec in ec_list:
                exist = 1
            else:
                exist = 0
            Results.append(str(ec) + '\t' + str(exist))

        fout.write('\n'.join(Results))
    print 'EC reconstruction for', SAMPLE, 'done.'


# Extract information for all samples
if __name__ == '__main__':
    buildDir(ECRESULTSDIR)
    getECs(SAMPLE, ECMAPPINGSDIR, ECRESULTSDIR, ECDIRNAME)
