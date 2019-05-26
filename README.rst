Reproduction
============

This section reproduces the output of [GuiltyTargets paper](https://www.biorxiv.org/content/10
.1101/521161v1).

Due to licencing reasons, analyses that use TTD drug targets and Alzheimer's disease data sets
are removed from this reproduction.

Requirements
============

You will need Python 3.7+ and R 3.6.0+ to run the program.

Required R packages are:
Bioconductor
Biobase
GEOquery
limma

To install the required Python libraries, you can run:

.. code-block:: bash

   $ cd reproduction
   $ pip install requirements.txt

Running
=======

To run the code:

.. code-block:: bash

   $ chmod +x run.sh
   $ ./run.sh

Output
======

You can find the output under reproduction/data
results.csv file gives an overview of all AUROC values under different settings.