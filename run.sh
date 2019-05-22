#!/bin/bash

mkdir data/aml
mkdir data/ipf
mkdir data/lc
mkdir data/ms
mkdir data/aml

# Download and prepare differential expression data
R CMD BATCH src/r_scripts/GSE32988.R
R CMD BATCH src/r_scripts/GSE24206.R
R CMD BATCH src/r_scripts/GSE30029.R
R CMD BATCH src/r_scripts/GSE36411_dhc.R
R CMD BATCH src/r_scripts/GSE36411_lc.R

# Download and prepare PPI networks
python3.7 src/reproduction/hippie_downloader.py

# Download and prepare targets
python3.7 src/reproduction/opentargets_downloader.py

# Rerun GuiltyTargets pipeline
python3.7 src/reproduction/guiltytargets_reproduction.py

# Crawl through the directories and summarize AUC results
# python3.7 src/reproduction/results_crawler.py
