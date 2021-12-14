import pandas as pd


def Run(df: pd.DataFrame,
        percentiles: list,
        include: list,
        exclude: list,
        datetime_is_numeric: bool) -> (pd.DataFrame, [False]):
    return df.describe(percentiles, include, exclude, datetime_is_numeric)
