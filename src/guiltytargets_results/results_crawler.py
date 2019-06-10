import os
from typing import Optional, TextIO

import pandas as pd

from .constants import mappings

__all__ = [
    'crawl_results',
]


def get_folders(parent_dir):
    contents = os.listdir(parent_dir)
    for name in contents:
        path = os.path.join(parent_dir, name)
        if not os.path.isfile(path) and name != "old":
            yield path


_MAIN_HEADER = [
    "Dataset",
    "PPI Network",
    "Target DB",
    "LFC Cutoff",
    "Confidence Cutoff",
    "Method",
    "AUC",
]


def crawl_results(*, data_dir, file: Optional[TextIO] = None) -> None:
    print(*_MAIN_HEADER, sep=',', file=file)

    result_folders = (
        result_folder
        for folder in get_folders(data_dir)
        for result_folder in get_folders(folder)
    )

    for result_folder in result_folders:
        parent_folder_path, folder_name = os.path.split(result_folder)
        _, dataset = os.path.split(parent_folder_path)

        try:
            _, graph, dtdb, lfc_cutoff, conf_cutoff = folder_name.split("-")
        except ValueError:
            print(f'Issue with folder name: {folder_name}')
            continue

        prefix = "{},{},{},{},{}".format(
            dataset,
            mappings[graph],
            mappings[dtdb],
            lfc_cutoff,
            conf_cutoff
        )

        gat2vec_auc_path = os.path.join(result_folder, "auc.tsv")
        try:
            auc_values = pd.read_csv(gat2vec_auc_path, sep="\t")["auc"].values.tolist()
        except Exception:
            print("No GuiltyTargets results in: ", result_folder)
            continue

        for auc in auc_values:
            print(prefix, 'GuiltyTargets', auc, sep=',', file=file)
