import pandas as pd
from typing import List, Dict, Type
from zero import SecretObject


def load_data(index : int) -> Type[SecretObject]:
    print(index)
    df = pd.read_csv("1_" + str(index) + ".csv")
    #return df_serialize(df)
    return SecretObject(df)


def get_mean(df_and_col: tuple) -> float:
    #df = df_deserialize(df_and_col[0])
    df = df_and_col[0]
    col = df_and_col[1]
    if df.shape[0] < 10:
        raise RuntimeError("Privacy rule violation: sample size too small")
    return df[col].mean()


def get_size(df : Type[SecretObject]) -> int:
    return df.shape[0]


def agg_mean(val_and_len : tuple) -> float:
    tot = 0
    mean_vals = val_and_len[0]
    sizes = val_and_len[1]
    for i in range(len(mean_vals)):
        tot += mean_vals[i]*sizes[i]
    return tot/sum(sizes)