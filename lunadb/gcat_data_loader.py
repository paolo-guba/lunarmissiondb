import pandas as pd

from lunadb.data_loader import DataLoader
from lunadb.gcat_catalog import GCATCatalog, GCATCatalogSelector


class GCATDataLoader(DataLoader):

    @classmethod
    def get_dataframe(cls, catalog: GCATCatalog) -> pd.DataFrame:
        with open(catalog., 'r') as f:
            header = f.readline().strip().split('\t')
            update_timestamp = f.readline().strip()

        return pd.read_csv(filepath, sep='\t', skiprows=2, names=header)


if __name__ == '__main__':
    satcat = GCATDataLoader.get_dataframe(GCATCatalogSelector.SATCAT)
    print()