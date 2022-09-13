import pandas as pd
from zero import SecretObject
from typing import Union, Type, Tuple, List
import numpy as np

def csv_to_df(data_id:str, sep_str:str) -> Type[SecretObject]:
    df = pd.read_csv(data_id, sep = sep_str)
    print(df)
    return SecretObject(df)

class rdf:
    def __init__(self, df):
        self.df = df
        self.shape = df.shape
        self.columns = df.columns
    
    def get_mean(self, a, b, levell=None, numeric_onlyy=None):
        return self.df.mean(axis=a, skipna=b, level=levell, numeric_only=numeric_onlyy)
    
    def describe(self, percentiless=None, includee=None, excludee=None, datetime_is_numericc=False):
        return self.df.describe(percentiles=percentiless, include=includee, exclude=excludee, datetime_is_numeric=datetime_is_numericc)
