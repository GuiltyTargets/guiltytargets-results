# -*- coding: utf-8 -*-

"""Utilities for GuiltyTargets-Results."""

import os

from mygene import MyGeneInfo
from opentargets import OpenTargetsClient

from guiltytargets.download import download_targets_for_disease
from .constants import DISEASE_ABBREVIATIONS, disease_efo_ids, opentargets_file_name

__all__ = [
    'download_targets_for_diseases',
]


def download_targets_for_diseases(data_dir: str):
    my_gene_info = MyGeneInfo()
    open_targets_client = OpenTargetsClient()
    for disease_efo_id, disease_abbreviation in zip(disease_efo_ids, DISEASE_ABBREVIATIONS):
        with open(os.path.join(data_dir, disease_abbreviation, opentargets_file_name), 'w+') as file:
            download_targets_for_disease(
                disease_efo_id=disease_efo_id,
                my_gene_info=my_gene_info,
                open_targets_client=open_targets_client,
                file=file,
            )
