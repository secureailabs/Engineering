import pandas as pd

def Run(series: pd.Series, normalize: bool, sort: bool, ascending: bool, bins: int, dropna: bool) -> (pd.Series, [False]):
    return series.value_counts(normalize, sort, ascending, bins, dropna)
