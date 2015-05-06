# Readme
These scripts allow you to annotate sequences from BLAST results (tabular output, BLAST protein coding amino acid sequences against KEGG database) - based on userdefined e-value, bitscore and identity thresholds - with KO numbers and summarize them in KEGG modules.  

Requirements: beautifulsoup4, requests  
  
## Instructions
```git clone https://github.com/pseudonymcp/keggmapping```

Use ```config.py``` to configure the output directories and organism groups for your analysis.  

1. Run ```buildKeggDB.py``` without parameters to download mapping files (gene ID to KO) for all organisms and the list of modules via KEGG REST API. You can specify 'Prokaryotes' and/or 'Eukaryotes' via the ```config.py``` file. You can run ```updateKeggDB.py``` anytime to re-download a new version of the module list and to update mapping files for organisms that were not included in the last download or should be remove (e.g. switching from Prokaryotes and Eukaryotes to Prokaryotes alone).  

2. Run ```annotate.py``` to annotate the BLAST result (with a specified max. e-value, min. bitscore and min. identity threshold) with KO numbers.  
__Usage:__ ```annotate.py <file> <max log e-value> <min bitscore> <min identity>```  

3. Run ```reconstructModule.py``` to reconstruct KEGG modules for KO numbers from the previous step. This script uses the KEGG Mapper Reconstruct Module webservices and parses the output. Results are stored as a textfile in a separate folder and can be used for further analyses (e.g. look at modules present/absent or complete/incomplete).  
__Usage:__ ```reconstructModule.py <KO mapping file>```  
  
## Explanation of codes assigned to modules
Number codes assigned should be read as:  

0 ... module complete  
1 ... 1 block missing  
2 ... 2 blocks missing  
3 ... module incomplete  
4 ... module not present  

## List amino acid sequences for a module of interest
There is an additional script ```module2seq.py``` that can be used to retrieve the amino acid sequences for each KO number within a module of interest. The results are written to std out.  

__Usage:__ ```module2seq.py <module> <KO mapping file> <protein sequence file>```  
