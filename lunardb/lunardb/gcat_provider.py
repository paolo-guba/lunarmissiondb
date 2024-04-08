from datetime import datetime

import httpx

from lunardb import DATA_DIR
from lunardb.lunardb.gcat_catalog import GCATCatalogSelector, GCATCatalog


class GCATCatalogProvider:
    GCAT_DIR = DATA_DIR / 'gcat'

    @classmethod
    def download_catalog(cls, catalog: GCATCatalog):
        with httpx.Client() as client:
            response = client.get(catalog.url)
            if response.status_code == 200:
                catalog.download_epoch = datetime.now()
                return response.text
            else:
                print("Failed to retrieve the URL:", response.status_code)

    @classmethod
    def save_catalog_to_file(cls, catalog: GCATCatalog):
        data = cls.download_catalog(catalog)
        with open(catalog.file_path, 'w') as f:
            f.write(data)

    @classmethod
    def update_all_catalogs(cls):
        for catalog in GCATCatalogSelector:
            cls.save_catalog_to_file(catalog.value)
