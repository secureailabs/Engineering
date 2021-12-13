import pandas as pd

def Run(df: pd.DataFrame, axis: int, how: str, thresh: int, subset: list, inplace: bool) -> (pd.DataFrame, [True]):
    return df.dropna(axis, how, thresh, subset, inplace)
