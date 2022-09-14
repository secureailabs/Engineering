import pandas as pd
from zero import SecretObject
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Union, Type, Tuple, List
import torch
import numpy as np

def csv_to_df(data_id:str, sep_str:str) -> Type[SecretObject]:
    df = pd.read_csv(data_id, sep = sep_str)
    return SecretObject(df)

def fit_transform(df: Type[SecretObject], col_label: str) -> Type[SecretObject]:
    e=LabelEncoder()
    for col in col_label:
        df[col] = e.fit_transform(df[col])
    return SecretObject(df)

def df_drop(df: Type[SecretObject], col_labels: Union[list, str]) -> Type[SecretObject]:
    new_df = df.drop(col_labels, axis = 1)
    return SecretObject(new_df)

def df_get_col(df: Type[SecretObject], col_labels: Union[list, str]) -> Type[SecretObject]:
    return SecretObject(df[col_labels])

def df_get_shape(df: Type[SecretObject]) -> Tuple[int]:
    return df.shape

def df_get_types(df: Type[SecretObject]) -> dict:
    return df.dtypes.to_dict()

def df_get_unique(df: Type[SecretObject]) -> dict:
    d = {}
    for col, column_series in df.iloc[:,1:].iteritems():
        d[col] = df[col].unique().tolist()
    return d

def df_get_col_names(df: Type[SecretObject]) -> List[str]:
    return df.columns.to_list()

def df_train_test_split(X: Type[SecretObject], y:Type[SecretObject], test_size: float) -> Tuple[Type[SecretObject]]:
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=42)
    return (SecretObject(x_train), SecretObject(x_test), SecretObject(y_train), SecretObject(y_test))

def df_to_torch_tensor(data: Type[SecretObject]) -> Type[SecretObject]:
    res = 0
    if isinstance(data, pd.DataFrame):
        res = torch.Tensor(data.values)
    if isinstance(data, pd.Series):
        res = torch.Tensor(np.transpose([data.values]))
    return SecretObject(res)
