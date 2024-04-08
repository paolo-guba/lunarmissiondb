from datetime import datetime, UTC

import pandas as pd

from lunardb.lunardb.gcat_catalog import GCATCatalog, GCATCatalogSelector


class GCATDataLoader:

    @classmethod
    def get_catalog(cls, catalog: GCATCatalog) -> GCATCatalog:
        with open(catalog.file_path, 'r') as f:
            header = f.readline().strip().split('\t')
            update_timestamp = f.readline().strip()
        update_timestamp = ' '.join(update_timestamp.split(' ')[2:])
        last_update_epoch = datetime.strptime(update_timestamp, '%Y %b %d %H:%M:%S')
        last_update_epoch = last_update_epoch.replace(tzinfo=UTC)
        catalog.last_update_epoch = last_update_epoch

        catalog.dataframe = pd.read_csv(catalog.file_path, sep='\t', skiprows=2, names=header, low_memory=False)
        return catalog

    @classmethod
    def get_satcat(cls) -> GCATCatalog:
        return cls.get_catalog(GCATCatalogSelector.SATCAT.value)

    @classmethod
    def get_auxcat(cls) -> GCATCatalog:
        return cls.get_catalog(GCATCatalogSelector.AUXCAT.value)

    @classmethod
    def get_ftocat(cls) -> GCATCatalog:
        return cls.get_catalog(GCATCatalogSelector.FTOCAT.value)


if __name__ == '__main__':
    satcat = GCATDataLoader.get_satcat()
    auxcat = GCATDataLoader.get_auxcat()
    ftocat = GCATDataLoader.get_ftocat()
