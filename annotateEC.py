#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Adds EC annotation to each gene ID that passes the specified thresholds
(max. e-value, min. bitscore, min. identity) in the BLAST results file.

Usage: annotateEC.py <file> <max log e-value> <min bitscore> <min identity>
"""
from config import *
import sys
import itertools
from collections import defaultdict
import urllib
import os
import errno
from buildKeggEC import buildOrgCodes

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    sys.exit(__doc__)

DATAFILE = sys.argv[1]
MAX_E = sys.argv[2]
MIN_BITSCORE = sys.argv[3]
MIN_IDENTITY = sys.argv[4]
# SAMPLE = re.search('(?<=/)\w+(?=\.)', DATAFILE).group()
SAMPLE = os.path.split(DATAFILE)[1] + '.'


def buildDir(dirname):
    """
    Prepare directory. Create directory if it does not exist.
    """
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(dirname):
            raise


def retrieveGeneEC(organism):
    """
    Build one gene ID to EC dictionary per organism.
    If the mapping file does not exist it will be downloaded via KEGG REST API.

    Input: organism code as string
    Output: Dictionary with gene ID as key and EC as value
    """
    try:
        f = open(ECDIRNAME + '/' + organism + '.txt', 'r')
    except:
        urllib.urlretrieve('http://rest.kegg.jp/link/enzyme/' + organism,
                           ECDIRNAME + '/' + organism + '.txt')
        f = open(ECDIRNAME + '/' + organism + '.txt', 'r')
    else:
        GENE_TO_EC = defaultdict(list)
        for line in f.readlines():
            if len(line.split('\t')) == 2 and len(line.split('\t')[1].split(':')) == 2:
               gene = line.split('\t')[0].strip()
               ec = line.split('\t')[1].split(':')[1].strip()
               GENE_TO_EC[gene].append(ec)
            else:
                   continue
        f.close()
        return GENE_TO_EC


def blastparser(filename, maxe, minbit, minid):
    """
    Parse BLAST output only for lines with e-value and bitscore above given
    thresholds. Build a dictionary with organism code as key and gene IDs with
    organism codes as values ('orgcode: geneid')
    """
    GENES = defaultdict(list)
    with open(filename, 'r') as f:
        for line in itertools.islice(f, 5, None):
            line = line.strip()
            if float(line.split('\t')[10]) < float(maxe) and \
               float(line.split('\t')[11]) > float(minbit) and \
               float(line.split('\t')[2]) > float(minid):
                gene = line.split('\t')[1]
                organism = gene.split(':')[0]
                query = line.split('\t')[0]
                GENES[organism].append((gene, query))
    return GENES


def annotateEC():
    try:
        os.remove(ECMAPPINGSDIR + '/' + SAMPLE + 'EC.txt')
    except OSError:
        pass
    finally:
        with open(ECMAPPINGSDIR + '/' + SAMPLE + 'EC.txt', 'a') as fmap:
            GENES = blastparser(DATAFILE, MAX_E, MIN_BITSCORE, MIN_IDENTITY)
            ORG_CODES = buildOrgCodes(ORGANISMGROUP)
            DONE = defaultdict(list)
            for organism in GENES:
                if organism in ORG_CODES:
                    geneToEC = retrieveGeneEC(organism)
                else:
                    continue
                if geneToEC is not None:
                    orgGenes = GENES[organism]
                    for entry in orgGenes:
                        gene = entry[0]
                        query = entry[1]
                        ec = geneToEC[gene]
                        if len(ec) == 0:
                            continue
                        elif len(ec) == 1:
                            if ec[0] not in DONE[query]:
                                DONE[query].append(ec[0])
                                fmap.write(query + '\t' + ec[0] + '\n')
                            else:
                                continue
                        else:
                            for ecitem in ec:
                                if ecitem not in DONE[query]:
                                    DONE[query].append(ecitem)
                                    fmap.write(query + '\t' + ecitem + '\n')
                                else:
                                    continue
                else:
                    continue
        print 'EC annotation for', SAMPLE, 'done.'

if __name__ == '__main__':
    buildDir(ECMAPPINGSDIR)
    annotateEC()
