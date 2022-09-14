import pandas as pd


def dataframe_serializer(df):
    return df.to_dict()


def dataframe_deserializer(df_dict):
    df = pd.DataFrame()
    return df.from_dict(df_dict)


def series_serializer(ser):
    return ser.to_dict()


def series_deserializer(ser_dict):
    ser = pd.Series(ser_dict)
    return ser
