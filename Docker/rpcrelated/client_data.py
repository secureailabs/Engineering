import pandas as pd

def client_csv_to_df(client, data_id, sep = ','):
    return client.call("csv_to_df", (data_id, sep))

def client_fit_transform(client, df, col_label):
    return client.call("fit_transform", (df, col_label))

def client_df_drop(client, df, col_labels):
    return client.call("df_drop", (df, col_labels))

def client_df_get_col(client, df, col_labels):
    return client.call("df_get_col", (df, col_labels))

def client_df_get_shape(client, df):
    return client.call("df_get_shape", df)

def client_df_get_types(client, df):
    res = client.call("df_get_types", df)
    return pd.Series(res)

def client_df_get_unique(client, df):
    return client.call("df_get_unique", df)

def client_df_get_col_names(client, df):
    return client.call("df_get_col_names", df)

def client_train_test_split(client, X, y, test_size):
    return client.call("df_train_test_split", (X, y, test_size))

def client_df_to_torch_tensor(client, data):
    return client.call("df_to_torch_tensor", data)