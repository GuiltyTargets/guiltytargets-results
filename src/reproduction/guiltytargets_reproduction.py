import itertools
import os
from guiltytargets.pipeline import run
from constants import *


def pipeline(input_directory, dge_path, ppi_graph_path, targets_path, lfc_cutoff, confidence_cutoff,
             results_suffix):
    output_path = os.path.join(input_directory, "Results-{}".format(results_suffix))

    dataset_name = "g2v"
    gat2vec_home = os.path.join(output_path, dataset_name)
    auc_output_path = os.path.join(output_path, 'auc.tsv')
    probs_output_path = os.path.join(output_path, 'probs.tsv')

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(gat2vec_home, exist_ok=True)

    print(input_directory,
          targets_path,
          ppi_graph_path,
          dge_path,
          auc_output_path,
          probs_output_path)

    run(input_directory,
        targets_path,
        ppi_graph_path,
        dge_path,
        auc_output_path,
        probs_output_path,
        max_adj_p=max_padj,
        max_log2_fold_change=lfc_cutoff * -1,
        min_log2_fold_change=lfc_cutoff,
        entrez_id_header=entrez_id_name,
        log2_fold_change_header=log_fold_change_name,
        adj_p_header=adjusted_p_value_name,
        base_mean_header=base_mean_name,
        entrez_delimiter=split_char,
        ppi_edge_min_confidence=confidence_cutoff)


def main():
    graph_paths = [hippie_path]
    target_paths = [ot_file]
    lfc_cutoffs = [0.5, 1.0, 1.5]
    confidence_cutoffs = [0.0, 0.63]
    input_folders = disease_abr
    real_mean_aucs = {}
    for input_folder in input_folders:
        input_path = os.path.join(data_dir, input_folder)
        dge_path = os.path.join(input_path, "DifferentialExpression.tsv")
        for graph_path, target_file_name, lfc_cutoff, conf_cutoff in itertools.product(
                graph_paths, target_paths, lfc_cutoffs, confidence_cutoffs):
            result_suffix = "h-" if graph_path == hippie_path else "s-"
            result_suffix += "t-" if target_file_name == ttd_file else "o-"
            result_suffix += str(lfc_cutoff)
            result_suffix += "-"
            result_suffix += str(conf_cutoff)

            conf_cutoff = conf_cutoff * 1000 if graph_path == string_path else conf_cutoff

            try:
                target_path = os.path.join(input_path, target_file_name)
                real_mean_aucs[input_folder] = pipeline(input_path,
                                                        dge_path,
                                                        graph_path,
                                                        target_path,
                                                        lfc_cutoff,
                                                        conf_cutoff,
                                                        result_suffix)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
