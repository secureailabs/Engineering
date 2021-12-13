import pandas as pd

def Run(df: pd.DataFrame, labels: list, axis: int, index: list, columns: list, level: int, inplace: bool, errors: str) -> (pd.DataFrame, [True]):
    return df.drop(labels, axis, index, columns, level, inplace, errors)
