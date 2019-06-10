# -*- coding: utf-8 -*-

"""Run the GuiltyTargets on several examples."""

import logging
import os
from itertools import product

from tqdm import tqdm

from guiltytargets.pipeline import run
from .constants import (
    adjusted_p_value_name, base_mean_name, disease_abbreviations, entrez_id_name, hippie_name, log_fold_change_name,
    max_padj, opentargets_file_name, split_char, string_name, ttd_file_name,
)

logger = logging.getLogger(__name__)


def pipeline(
        *,
        input_directory,
        dge_path,
        ppi_graph_path,
        targets_path,
        lfc_cutoff,
        confidence_cutoff,
        results_suffix,
):
    output_path = os.path.join(input_directory, f"Results-{results_suffix}")

    dataset_name = "g2v"
    gat2vec_home = os.path.join(output_path, dataset_name)
    auc_output_path = os.path.join(output_path, 'auc.tsv')
    probs_output_path = os.path.join(output_path, 'probs.tsv')

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(gat2vec_home, exist_ok=True)

    print(
        input_directory,
        targets_path,
        ppi_graph_path,
        dge_path,
        auc_output_path,
        probs_output_path,
    )

    run(
        input_directory,
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
        ppi_edge_min_confidence=confidence_cutoff,
    )


def main(*, data_dir, graph_paths, use_tqdm: bool = True):
    target_paths = [opentargets_file_name]
    lfc_cutoffs = [0.5, 1.0, 1.5]
    confidence_cutoffs = [0.0, 0.63]
    it = product(graph_paths, target_paths, lfc_cutoffs, confidence_cutoffs, disease_abbreviations)
    if use_tqdm:
        it = tqdm(it)
    for graph_path, target_path, lfc_cutoff, confidence_cutoff, input_folder in it:
        input_path = os.path.join(data_dir, input_folder)
        dge_path = os.path.join(input_path, "DifferentialExpression.tsv")

        result_suffix = "h-" if graph_path.endswith(hippie_name) else "s-"
        result_suffix += "t-" if target_path == ttd_file_name else "o-"
        result_suffix += str(lfc_cutoff)
        result_suffix += "-"
        result_suffix += str(confidence_cutoff)

        confidence_cutoff = confidence_cutoff * 1000 if graph_path.endswith(string_name) else confidence_cutoff

        try:
            pipeline(
                input_directory=input_path,
                dge_path=dge_path,
                ppi_graph_path=graph_path,
                targets_path=os.path.join(input_path, target_path),
                lfc_cutoff=lfc_cutoff,
                confidence_cutoff=confidence_cutoff,
                results_suffix=result_suffix,
            )
        except Exception:
            logging.exception(f'Failed for {graph_path} {target_path} {lfc_cutoff} {confidence_cutoff}')
