# -*- coding: utf-8 -*-

"""CLI for GuiltyTargets-Results."""

import os

import click

from .constants import hippie_name, hippie_url
from .guiltytargets_reproduction import main as gt_main
from .results_crawler import crawl_results
from .utils import download_hippie, download_targets_for_diseases


@click.command()
@click.option('-d', '--data-dir', type=click.Path(dir_okay=True, file_okay=False))
def main(data_dir):
    """Run an evaluation of GuiltyTargets."""
    download_hippie(url=hippie_url, data_dir=data_dir)
    download_targets_for_diseases(data_dir)

    hippie_path = os.path.join(data_dir, hippie_name)
    # Run pipeline
    gt_main(
        data_dir=data_dir,
        graph_paths=[hippie_path],
    )

    # Run results crawler
    crawl_results(data_dir=data_dir)


if __name__ == '__main__':
    main()
