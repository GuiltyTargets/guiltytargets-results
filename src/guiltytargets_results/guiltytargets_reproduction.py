# -*- coding: utf-8 -*-

"""Run the GuiltyTargets on several examples."""

import logging
import os
from itertools import product

from tqdm import tqdm

from guiltytargets.pipeline import run
from .constants import (
    DISEASE_ABBREVIATIONS, adjusted_p_value_name, base_mean_name, entrez_id_name, hippie_name, log_fold_change_name,
    max_padj, opentargets_file_name, split_char, string_name, ttd_file_name,
)

__all__ = ['main']

logger = logging.getLogger(__name__)

LFC_CUTOFFS = [0.5, 1.0, 1.5]
CONFIDENCE_CUTOFFS = [0.0, 0.63]


def main(*, data_dir, graph_paths, use_tqdm: bool = True):
    target_paths = [opentargets_file_name]

    it = product(
        DISEASE_ABBREVIATIONS,
        graph_paths,
        target_paths,
        LFC_CUTOFFS,
        CONFIDENCE_CUTOFFS,
    )
    total = len(graph_paths) * len(target_paths) * len(LFC_CUTOFFS) * len(CONFIDENCE_CUTOFFS) * len(
        DISEASE_ABBREVIATIONS)
    if use_tqdm:
        it = tqdm(it, total=total)
    for disease_abbreviation, ppi_graph_path, target_path, lfc_cutoff, confidence_cutoff in it:
        result_suffix = "h-" if ppi_graph_path.endswith(hippie_name) else "s-"
        result_suffix += "t-" if target_path == ttd_file_name else "o-"
        result_suffix += str(lfc_cutoff)
        result_suffix += "-"
        result_suffix += str(confidence_cutoff)

        confidence_cutoff = confidence_cutoff * 1000 if ppi_graph_path.endswith(string_name) else confidence_cutoff

        input_directory = os.path.join(data_dir, disease_abbreviation)

        dge_path = os.path.join(input_directory, "DifferentialExpression.tsv")
        if not os.path.exists(dge_path):
            it.write(f'Skipping due to missing DGE file: {dge_path}')
            continue

        targets_path = os.path.join(input_directory, target_path)
        if not os.path.exists(targets_path):
            it.write(f'Skipping due to missing targets file: {targets_path}')
            continue

        output_path = os.path.join(input_directory, f"Results-{result_suffix}")
        if os.path.exists(output_path):
            it.write(f'Skipping because already ran: {output_path}')
            continue

        dataset_name = "g2v"
        gat2vec_home = os.path.join(output_path, dataset_name)
        auc_output_path = os.path.join(output_path, 'auc.tsv')
        probs_output_path = os.path.join(output_path, 'probs.tsv')

        os.makedirs(output_path, exist_ok=True)
        os.makedirs(gat2vec_home, exist_ok=True)

        it.write(f"""Working on:
  input:  {input_directory}
  target: {targets_path}
  dge:    {dge_path}
  graph:  {ppi_graph_path}""")

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
