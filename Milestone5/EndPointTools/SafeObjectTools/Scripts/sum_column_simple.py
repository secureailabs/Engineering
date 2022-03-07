import pandas as pd


def Run(df: pd.DataFrame,
        col: str) -> (int, [True]):
    return int(df[col].sum())
