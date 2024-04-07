from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import pandas as pd

from lunadb import DATA_DIR


@dataclass
class GCATCatalog:
    name: str
    description: str
    dataframe: pd.DataFrame = None
    last_update_epoch: datetime = None
    download_epoch: datetime = None
    base_url = 'https://planet4589.org/space/gcat/'
    directory = 'gcat'
    file_format = 'tsv'

    @property
    def url(self):
        return f'{self.base_url}/tsv/cat/{self.name}.tsv'

    @property
    def file_path(self):
        return DATA_DIR / self.directory / f'{self.name}.{self.file_format}'


class GCATCatalogSelector(Enum):
    SATCAT = GCATCatalog('satcat', 'Satellite Catalog')
    AUXCAT = GCATCatalog('auxcat', 'Auxiliary Catalog')
    FTOCAT = GCATCatalog('ftocat', 'Failed-to-orbit Catalog')
    TMPCAT = GCATCatalog('tmpcat', 'Temporary Catalog')
    CSOCAT = GCATCatalog('csocat', 'Complementary Space Object Catalog')
    ECAT = GCATCatalog('ecat', 'Event Catalog')
