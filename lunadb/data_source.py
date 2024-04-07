from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

from lunadb import DATA_DIR


@dataclass
class DataSource:
    name: str
    description: str
    base_url: str = None
    directory: str = None
    dataframe: pd.DataFrame = None
    last_update_epoch: datetime = None
    download_epoch: datetime = None

    @staticmethod
    def _get_filepath(folder_name: str, file_name: str, file_format: str = 'csv') -> Path:
        return DATA_DIR / folder_name / f'{file_name}.{file_format}'

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    @abstractmethod
    def filepath(self) -> Path:
        pass
