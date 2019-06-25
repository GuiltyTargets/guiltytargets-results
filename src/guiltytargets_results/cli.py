# -*- coding: utf-8 -*-

"""CLI for GuiltyTargets-Results."""

import os

import click

from guiltytargets.download import download_hippie
from .constants import hippie_name, hippie_url
from .download import download_targets_for_diseases
from .guiltytargets_reproduction import main as gt_main
from .results_crawler import crawl_results


@click.command()
@click.option('-d', '--directory', type=click.Path(dir_okay=True, file_okay=False),
              help='Data directory')
def main(directory):
    """Run an evaluation of GuiltyTargets."""
    hippie_path = os.path.join(directory, hippie_name)

    download_hippie(url=hippie_url, path=hippie_path)
    download_targets_for_diseases(directory)

    # Run pipeline
    gt_main(
        data_dir=directory,
        graph_paths=[hippie_path],
    )

    # Run results crawler
    crawl_results(directory=directory)


if __name__ == '__main__':
    main()
