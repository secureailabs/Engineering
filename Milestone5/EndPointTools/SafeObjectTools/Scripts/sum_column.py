import pandas as pd


def Run(df: pd.DataFrame,
        col: str,
        dummy_ds: str) -> (int, [True]):
    return int(df[col].sum())
