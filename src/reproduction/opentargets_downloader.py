import os

import mygene
from opentargets import OpenTargetsClient
from constants import disease_abr, disease_ids_efo, data_dir, ot_file


def download_for_disease(disease_id, outpath):
    ot = OpenTargetsClient()
    assoc = ot.get_associations_for_disease(
        disease_id,
        fields=['associationscore.datatypes', 'target.id']
    ).filter(
        datatype='known_drug'
    )
    ensembl_list = [a['target']['id'] for a in assoc]

    mg = mygene.MyGeneInfo()
    id_mappings = mg.getgenes(ensembl_list, fields="entrezgene")

    with open(outpath, 'w+') as outfile:
        for mapping in id_mappings:
            if 'entrezgene' in mapping.keys():
                outfile.write(mapping['entrezgene'])
                outfile.write('\n')


if __name__ == '__main__':
    for (id, abr) in zip(disease_ids_efo, disease_abr):
        outpath = os.path.join(data_dir, abr, ot_file)
        download_for_disease(id, outpath)
