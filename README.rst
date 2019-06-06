Reproduction
============
This section reproduces the output of `GuiltyTargets paper
<https://www.biorxiv.org/content/10.1101/521161v1>`_

Due to licensing reasons, analyses that use TTD drug targets and
Alzheimer's disease data sets have been removed from this
reproduction.

Installation
------------
You will need Python 3.7+ and R 3.6.0+ to run the program.

The required R packages are:

- Bioconductor
- Biobase
- GEOquery
- limma

To install the required Python libraries, you can run:

.. code-block:: sh

   $ git clone https://github.com/GuiltyTargets/reproduction.git
   $ cd reproduction
   $ pip install -e .

Running
-------
To run the code:

.. code-block:: sh

   $ source run.sh

Output
------
You can find the output under reproduction/data. The ``results.csv``
file gives an overview of all AUROC values under different settings.
