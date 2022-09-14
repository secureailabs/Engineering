import seaborn as sns
from zero import SecretObject
import io
import matplotlib.pyplot as plt
from typing import Type
import dataframe_image as dfi

def _convert_to_bin(figure):
    if isinstance(figure, io.BytesIO):
        figure.seek(0)
        res  = figure.read()
        figure.close()
        return res
    buf = io.BytesIO()
    figure.savefig(buf, dpt = 300, format = "png", backend = "agg")
    buf.seek(0)
    res = buf.read()
    buf.close()
    plt.close('all')
    return res

def plot_countplot(col_label: str, df: Type[SecretObject]) -> bytes:
    figure = sns.countplot(x=col_label, data=df)
    return _convert_to_bin(figure.figure)

def plot_hist(df: Type[SecretObject]) -> bytes:
    df.hist(figsize=(20,15));
    fig = plt.gcf()
    return _convert_to_bin(fig)

def plot_corr(df: Type[SecretObject]) -> dict:
    corr=df.corr()
    df_dict = {}
    df_dict['data'] = corr.values.tolist()
    df_dict['index'] = list(corr.index)
    df_dict['columns'] = list(corr.columns)
    #df_styled = corr.style.background_gradient(cmap='coolwarm',axis=None)
    #buf = io.BytesIO()
    #dfi.export(df_styled, buf)
    return df_dict

def plot_miss(df: Type[SecretObject]) -> bytes:
    figure = sns.displot(data=df.isna().melt(value_name="missing"), y="variable", hue="missing", multiple="fill", aspect=1.25)
    return _convert_to_bin(figure.figure)

