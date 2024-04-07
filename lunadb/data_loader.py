from abc import abstractmethod

import pandas as pd


class DataLoader:
    @classmethod
    @abstractmethod
    def get_dataframe(cls, *args, **kwargs) -> pd.DataFrame:
        pass
