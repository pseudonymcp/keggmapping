# Readme
These scripts allow you to annotate sequences from BLAST results (tabular output, BLAST against KEGG database) based on userdefined e-value, bitscore and identity thresholds with KO numbers and summarize them in KEGG modules.  

## Instructions
1. Run __buildKeggDB.py__ without parameters to download mapping files (gene ID to KO) for all organisms and the list of modules via KEGG REST API. You can specify 'Prokaryotes' and/or 'Eukaryotes' via the __config.py__ file. You can run __updateKeggDB.py__ anytime to re-download a new version of the module list and to update mapping files for organisms that were not included in the last download.
2. Run __annotate.py__ to annotate BLAST results (with a specified max. e-value, min. bitscore and min. identity) with KO numbers.  
Usage: ```annotate.py <file> <max log e-value> <min bitscore> <min identity>```
3. Run __reconstructModule.py__ to reconstruct KEGG modules for KO numbers from the previous step. This script uses the KEGG Mapper Reconstruct Module webservices and parses the output. Results are stored as textfiles in a separate folder and can be used for further analyses (e. g. look at modules present/absent or complete/incomplete).  
Usage: ```reconstructModule.py <KO mapping file>```
  
#### Explanation of codes assigned to modules
Number codes assigned should be read as:  
0 ... module complete  
1 ... 1 block missing  
2 ... 2 blocks missing  
3 ... module incomplete  
4 ... module not present  