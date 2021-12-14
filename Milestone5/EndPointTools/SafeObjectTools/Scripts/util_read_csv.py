from io import StringIO
import pandas as pd


def Run(csvFilename: str) -> (pd.DataFrame, [True]):
    csv = StringIO(csvFilename.decode().replace('\r', ''))
    df = pd.read_csv(csv, sep='\x1f', error_bad_lines=False)
    return df
