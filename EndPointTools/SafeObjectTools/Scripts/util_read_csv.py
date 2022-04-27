from io import StringIO
import pandas as pd


def Run(csvFilename: str) -> pd.DataFrame:
    """
    Read a csv file and output a dataframe
    ###Args:
    `csvFilename`: data identifier of the csv file
    ###Returns:
    The result dataframe, confidentiality set to True 
    Confidentiality:True
    """
    csv = StringIO(csvFilename.decode().replace('\r', ''))
    df = pd.read_csv(csv, sep='\x1f', error_bad_lines=False)
    return df
