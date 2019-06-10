# -*- coding: utf-8 -*-

"""Utilities for GuiltyTargets-Results."""

import io
import os
from typing import Optional, TextIO

import pandas as pd
import requests
from mygene import MyGeneInfo
from opentargets import OpenTargetsClient

from .constants import disease_abbreviations, disease_efo_ids, hippie_name, opentargets_file_name

__all__ = [
    'download_hippie',
    'download_targets_for_diseases',
    'download_targets_for_disease',
]


def download_hippie(*, url, data_dir):
    s = requests.get(url).content
    cols = ['symbol1', 'entrez1', 'symbol2', 'entrez2', 'confidence', 'description']
    df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep='\t', header=None, names=cols)
    hippie_path = os.path.join(data_dir, hippie_name)
    df[['entrez1', 'entrez2', 'confidence']].to_csv(hippie_path, sep='\t', header=False, index=False)


def download_targets_for_diseases(data_dir: str):
    my_gene_info = MyGeneInfo()
    open_targets_client = OpenTargetsClient()
    for disease_efo_id, disease_abbreviation in zip(disease_efo_ids, disease_abbreviations):
        with open(os.path.join(data_dir, disease_abbreviation, opentargets_file_name), 'w+') as file:
            download_targets_for_disease(
                disease_efo_id=disease_efo_id,
                my_gene_info=my_gene_info,
                open_targets_client=open_targets_client,
                file=file,
            )


def download_targets_for_disease(
        disease_efo_id: str,
        open_targets_client: Optional[OpenTargetsClient] = None,
        my_gene_info: Optional[MyGeneInfo] = None,
        file: Optional[TextIO] = None,
) -> None:
    """

    :param disease_efo_id: A disease's EFO identifier
    :param outpath:
    :param open_targets_client: An OpenTargetsClient
    :param my_gene_info: A MyGeneInfo client
    """
    if open_targets_client is None:
        open_targets_client = OpenTargetsClient()
    associations = open_targets_client.get_associations_for_disease(
        disease_efo_id,
        fields=[
            'associationscore.datatypes',
            'target.id',
        ],
    ).filter(
        datatype='known_drug',
    )
    ensembl_list = [
        association['target']['id']
        for association in associations
    ]

    if my_gene_info is None:
        my_gene_info = MyGeneInfo()

    id_mappings = my_gene_info.getgenes(ensembl_list, fields="entrezgene")

    for mapping in id_mappings:
        if 'entrezgene' in mapping.keys():
            print(mapping['entrezgene'], file=file)
