#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Adds KO annotation to each gene ID that passes the specified thresholds
(max. e-value, min. bitscore, min. identity) in the BLAST results file.

Usage: annotate.py <file> <max log e-value> <min bitscore> <min identity>
"""
from config import *
import sys
import itertools
from collections import defaultdict
import urllib
import os
import errno
from buildKeggDB import buildOrgCodes

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


def retrieveGeneKO(organism):
    """
    Build one gene ID to KO dictionary per organism.
    If the mapping file does not exist it will be downloaded via KEGG REST API.

    Input: organism code as string
    Output: Dictionary with gene ID as key and KO as value
    """
    try:
        f = open(KEGGDIRNAME + '/' + organism + '.txt', 'r')
    except:
        urllib.urlretrieve('http://rest.kegg.jp/link/ko/' + organism,
                           KEGGDIRNAME + '/' + organism + '.txt')
        f = open(KEGGDIRNAME + '/' + organism + '.txt', 'r')
    else:
        GENE_TO_KO = defaultdict(list)
        for line in f.readlines():
            gene = line.split('\t')[0].strip()
            ko = line.split('\t')[1].split(':')[1].strip()
            GENE_TO_KO[gene].append(ko)
        f.close()
        return GENE_TO_KO


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


def annotateKO():
    try:
        os.remove(MAPPINGSDIR + '/' + SAMPLE + 'KO.txt')
    except OSError:
        pass
    finally:
        with open(MAPPINGSDIR + '/' + SAMPLE + 'KO.txt', 'a') as fmap:
            GENES = blastparser(DATAFILE, MAX_E, MIN_BITSCORE, MIN_IDENTITY)
            ORG_CODES = buildOrgCodes(ORGANISMGROUP)
            for organism in GENES:
                if organism in ORG_CODES:
                    geneToKO = retrieveGeneKO(organism)
                else:
                    continue
                if geneToKO is not None:
                    orgGenes = GENES[organism]
                    for entry in orgGenes:
                        gene = entry[0]
                        query = entry[1]
                        ko = geneToKO[gene]
                        if len(ko) == 0:
                            continue
                        elif len(ko) == 1:
                            fmap.write(query + '\t' + ko[0] + '\n')
                        else:
                            for koitem in ko:
                                fmap.write(query + '\t' + koitem + '\n')
                else:
                    continue
        print 'Annotation for', SAMPLE, 'done.'

if __name__ == '__main__':
    buildDir(MAPPINGSDIR)
    annotateKO()
