import pandas as pd
import io
import requests

from constants import hippie_path, hippie_url


def download_hippie(url, out_path):
    s = requests.get(url).content
    cols = ['symbol1', 'entrez1', 'symbol2', 'entrez2', 'confidence', 'description']
    df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep='\t', header=None, names=cols)
    df[['entrez1', 'entrez2', 'confidence']].to_csv(out_path, sep='\t', header=False, index=False)


if __name__ == '__main__':
    download_hippie(hippie_url, hippie_path)
