import pandas as pd
import torch


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
    """
    To do proxy deserialization

    :param proxy_dict: proxy dictionary
    :type proxy_dict: dict
    """
    pass


def torch_nn_serializer(model):
    """
    serialize torch linear model to dict

    :param model: torch nn model
    :type model: torch.nn.Module
    :return: state dictionary
    :rtype: dict
    """
    model_dict = model.state_dict()
    for key in model_dict:
        if isinstance(model_dict[key], torch.Tensor):
            model_dict[key] = {
                "_type_": str(torch.Tensor),
                "val": model_dict[key].tolist(),
            }
    return model_dict


def torch_nn_deserializer(model_dict):
    """
    deserialize torch model from a dict with list to dict with tensors

    :param model_dict: state dictionary
    :type model_dict: dict
    :return: dictionary containing tensors
    :rtype: dict
    """
    for key in model_dict:
        if isinstance(model_dict[key], dict) and model_dict[key]["_type_"] == str(torch.Tensor):
            model_dict[key] = torch.FloatTensor(model_dict[key]["val"])

    return model_dict


serializer_table = {
    str(pd.DataFrame): dataframe_serializer,
    str(pd.Series): series_serializer,
    "proxy": proxy_serializer,
    str(torch.nn.Module): torch_nn_serializer,
}

deserializer_table = {
    str(pd.DataFrame): dataframe_deserializer,
    str(pd.Series): series_deserializer,
    "proxy": proxy_deserializer,
    str(torch.nn.Module): torch_nn_deserializer,
}
