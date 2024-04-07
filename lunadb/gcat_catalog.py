from dataclasses import dataclass
from enum import Enum

from lunadb.data_source import DataSource


@dataclass
class GCATCatalog(DataSource):
    base_url = 'https://planet4589.org/space/gcat/'
    directory = 'gcat'

    @property
    def url(self):
        return f'{self.base_url}/tsv/cat/{self.name}.tsv'


class GCATCatalogSelector(Enum):
    SATCAT = GCATCatalog('satcat', 'Satellite Catalog')
    AUXCAT = GCATCatalog('auxcat', 'Auxiliary Catalog')
    FTOCAT = GCATCatalog('ftocat', 'Failed-to-orbit Catalog')
    TMPCAT = GCATCatalog('tmpcat', 'Temporary Catalog')
    CSOCAT = GCATCatalog('csocat', 'Complementary Space Object Catalog')
    ECAT = GCATCatalog('ecat', 'Event Catalog')

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
