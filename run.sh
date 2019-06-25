#!/bin/bash

mkdur -p data/
mkdir -p data/aml/
mkdir -p data/ipf/
mkdir -p data/lc/
mkdir -p data/ms/
mkdir -p data/hc/

# Download and prepare differential expression data
Rscript R/GSE32988.R
Rscript R/GSE24206.R
Rscript R/GSE30029.R
Rscript R/GSE36411_dhc.R
Rscript R/GSE36411_lc.R

python --version
python -m guiltytargets_results -d data/
