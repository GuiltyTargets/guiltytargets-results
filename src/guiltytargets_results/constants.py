# -*- coding: utf-8 -*-

"""CLI for GuiltyTargets results."""

import os

# generic
data_dir = 'data'

mappings = {
    'h': 'HIPPIE',
    's': 'STRING',
    't': 'Therapeutic Targets',
    'o': 'Open Targets',
}

disease_abbreviations = [
    'aml',  # acute myeloid leukemia
    'hc',  # hepatocellular carcinoma
    'ipf',  # idiopathic pulmonary fibrosis
    'lc',  # cirrhosis of liver
    'ms',  # multiple sclerosis
]
# for targets
disease_efo_ids = [
    'EFO_0000222',  # acute myeloid leukemia
    'EFO_0000182',  # hepatocellular carcinoma
    'EFO_0000768',  # idiopathic pulmonary fibrosis
    'EFO_0001422',  # cirrhosis of liver
    'EFO_0003885',  # multiple sclerosis
]
ttd_file_name = 'ttd_entrez.txt'
opentargets_file_name = 'ot_entrez.txt'

# for ppi graphs
hippie_url = 'http://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/hippie_current.txt'
hippie_name = 'hippie.edgelist'

string_url = 'http://string-db.org/api/tsv/resolve?species=9606'
string_name = 'string.edgelist'

# for differential expression
max_padj = 0.05
base_mean_name = None
log_fold_change_name = 'logFC'
adjusted_p_value_name = 'adj.P.Val'
entrez_id_name = 'Gene.ID'
split_char = '///'
diff_type = 'all'
