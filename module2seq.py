#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: python module2seq.py <module> <path to ko file> <path to proteins file>
"""
import urllib
import os
import sys
from collections import defaultdict

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    sys.exit(__doc__)

URL_MODULES = 'http://www.kegg.jp/kegg-bin/download_htext?htext=ko00002.keg&'\
              'format=htext'

#MODULE = 'M00549'
#KO_FILE = './data/YL2.coding.faa.vs.KEGG.rapsearch.m8.KO.txt'
#SEQ_FILE = './data/YL2.coding.faa'
MODULE = str(sys.argv[1])
KO_FILE = sys.argv[2]
SEQ_FILE = sys.argv[3]


def buildModuleDict():
    if os.path.isfile('./ko00002.keg'):
        pass
    else:
        urllib.urlretrieve(URL_MODULES, 'ko00002.keg')
    modules = defaultdict(list)
    with open('ko00002.keg', 'r') as fin:
        content = fin.readlines()
        for i in range(0, len(content)):
            if content[i][1:].lstrip().startswith('M00'):
                module = content[i][1:].lstrip().split()[0]
                i += 1
                while content[i][1:].lstrip().startswith('K') and\
                      len(content[i][1:].lstrip().split()[0]) == 6:
                    modules[module].append(content[i][1:].lstrip().split()[0])
                    i += 1
        return modules


def buildKODict():
    kos = defaultdict(list)
    modules = buildModuleDict()
    for module in modules:
        for ko in modules[module]:
            kos[ko].append(module)
    return kos


def getKOsPerModule(module):
    modules = buildModuleDict()
    return modules[module]


def getGeneID(module, kofile):
    geneIDforKO = defaultdict(list)
    kos = getKOsPerModule(module)
    with open(kofile, 'r') as fin:
        for line in fin.readlines():
            ko = line.split()[1]
            geneid = line.split()[0]
            if ko in kos:
                if geneid not in geneIDforKO[ko]:
                    geneIDforKO[ko].append(line.split()[0])
    return geneIDforKO


def getSeqForKO(module, kofile, seqfile):
    seqForGeneID = defaultdict(str)
    geneIDforKO = getGeneID(module, kofile)
    with open(seqfile, 'r') as fin:
        content = fin.readlines()
        for i in range(0, len(content)):
            if content[i].startswith('>'):
                geneID = content[i].split()[0][1:]
                seqForGeneID[geneID] = ''
                i += 1
            else:
                seqForGeneID[geneID] = seqForGeneID[geneID] +\
                    content[i].strip()
                i += 1
    for ko in geneIDforKO:
        for gene in geneIDforKO[ko]:
            print ko + ':', gene, '\n', seqForGeneID[gene], '\n'


def getKOs(kofile):
    kopresent = []
    with open(kofile, 'r') as fin:
        for line in fin.readlines():
            kopresent.append(line.split()[1])
    return kopresent


if __name__ == '__main__':
    getSeqForKO(MODULE, KO_FILE, SEQ_FILE)
    print '\n# The following KOs from module', MODULE, 'are present '\
          'in this sample and appear in these modules:\n'
    kos = buildKODict()
    results = []
    kopresent = getKOs(KO_FILE)
    for ko in getKOsPerModule(MODULE):
        if ko in kopresent:
            tmp = '# ' + ko + ': ' + ', '.join(sorted(kos[ko]))
            results.append(tmp)
    print '\n'.join(sorted(results))
