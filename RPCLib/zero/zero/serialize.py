import pandas as pd


def dataframe_serializer(df):
    """
    serialize dataframe to dict

    :param df: dataframe to be converted
    :type df: pd.DataFrame
    :return: dict
    :rtype: dict
    """
    df_dict = df.to_dict()
    df_dict["__type__"] = str(type(df))
    return df_dict


def dataframe_deserializer(df_dict):
    """
    deserialize dict to dataframe

    :param df_dict: dict
    :type df_dict: dict
    :return: dataframe
    :rtype: pd.DataFrame
    """
    df_dict.pop("__type__")
    df = pd.DataFrame()
    return df.from_dict(df_dict)


def series_serializer(ser):
    """
    serialize series to dict

    :param ser: series
    :type ser: pd.Series
    :return: dict
    :rtype: dict
    """
    ser_dict = ser.to_dict()
    ser_dict["__type__"] = str(type(ser))
    return ser_dict


def series_deserializer(ser_dict):
    """
    deserialize dict to series

    :param ser_dict: dict
    :type ser_dict: dict
    :return: series
    :rtype: pd.Series
    """
    ser_dict.pop("__type__")
    ser = pd.Series(ser_dict)
    return ser


def proxy_serializer(proxy):
    """
    serialize a proxy object

    :param proxy: proxy object  to be serialized
    :type proxy: Proxy
    """
    msg = {}
    msg["id"] = proxy._roid
    msg["type"] = proxy._rotype
    msg["object"] = 1
    return msg


def proxy_deserializer(proxy_dict):
    pass


serializer_table = {
    str(pd.DataFrame): dataframe_serializer,
    str(pd.Series): series_serializer,
    "proxy": proxy_serializer,
}

deserializer_table = {
    str(pd.DataFrame): dataframe_deserializer,
    str(pd.Series): series_deserializer,
    "proxy": proxy_deserializer,
}
