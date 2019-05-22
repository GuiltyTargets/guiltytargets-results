import os

# generic
data_dir = 'data'
disease_abr = ['aml', 'hc', 'ipf', 'lc', 'ms']
mappings = {
    'h': 'HIPPIE',
    's': 'STRING',
    't': 'Therapeutic Targets',
    'o': 'Open Targets'
}

# for targets
disease_ids_efo = ['EFO_0000222', 'EFO_0000182', 'EFO_0000768', 'EFO_0001422',
                   'EFO_0003885']
ttd_file = 'ttd_entrez.txt'
ot_file = 'ot_entrez.txt'

# for ppi graphs
hippie_url = 'http://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/hippie_current.txt'
hippie_path = os.path.join(data_dir, 'hippie.edgelist')
string_url = 'http://string-db.org/api/tsv/resolve?species=9606'
string_path = os.path.join(data_dir, 'string.edgelist')

# for differential expression
max_padj = 0.05
base_mean_name = None
log_fold_change_name = 'logFC'
adjusted_p_value_name = 'adj.P.Val'
entrez_id_name = 'Gene.ID'
split_char = '///'
diff_type = 'all'

# for results_crawler
output_file_path = os.path.join(data_dir, 'results.csv')
