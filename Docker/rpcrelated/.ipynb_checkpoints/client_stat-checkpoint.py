#safe function rpc interface:
def client_chi_square(client, sample_0, sample_1):
    return client.call("chi_square", (sample_0, sample_1))

def client_chi_square_agg(client, list_precompute):
    return client.call("chi_square_agg", list_precompute)

def client_kolmogorov_smirnovdef(client, sample_0, sample_ranked_0, distribution, count_total):
    return client.call("kolmogorov_smirnovdef", (sample_0, sample_ranked_0, distribution, count_total))

def client_kolmogorov_smirnovdef_agg(client, list_precompute):
    return client.call("kolmogorov_smirnovdef_agg", list_precompute)

def client_levene(client, sample_0_series, sample_1_series, mean_0, mean_1):
    return client.call("levene", (sample_0_series, sample_1_series, mean_0, mean_1))

def client_levene_agg(client, list_list_precompute, equal_varriances = False):
    return client.call("levene_agg", (list_list_precompute, equal_varriances))

def client_mann_whitney(client, series_0, series_concatenated_ranked):
    return client.call("mann_whitney", (series_0, series_concatenated_ranked))

def client_mann_whitney_agg(client, list_precompute):
    return client.call("mann_whitney_agg", list_precompute)

def client_paired_t(client, sample_0_series, sample_1_series):
    return client.call("paired_t", (sample_0_series, sample_1_series))

def client_paired_t_agg(client, list_list_precompute):
    return client.call("paired_t_agg", list_list_precompute)

def client_unpaired_t(client, sample_0_series, sample_1_series):
    return client.call("unpaired_t", (sample_0_series, sample_1_series))

def client_unpaired_t_agg(client, list_list_precompute, equal_varriances=False):
    return client.call("unpaired_t_agg", (list_list_precompute, equal_varriances))

def client_wilcoxon_signed_rank(client, sample_difference, sample_absolute_difference_ranked):
    return client.call("wilcoxon_signed_rank", (sample_difference, sample_absolute_difference_ranked))

def client_wilcoxon_signed_rank_agg(client, list_precompute):
    return client.call("wilcoxon_signed_rank_agg", list_precompute)

def client_kurtosis(client, sample_0_dataframe):
    return client.call("kurtosis", sample_0_dataframe)

def client_kurtosis_agg(client, list_list_precompute):
    return client.call("kurtosis_agg", list_list_precompute)

def client_mean(client, sample_0_dataframe):
    return client.call("mean", sample_0_dataframe)

def client_mean_agg(client, list_list_precompute):
    return client.call("mean_agg", list_list_precompute)

def client_min_max(client, series_sample):
    return client.call("min_max", series_sample)

def client_min_max_agg(client, list_tuple_min_max):
    return client.call("min_max_agg", list_tuple_min_max)

def client_pearson(client, sample_0_dataframe, sample_1_dataframe):
    return client.call("pearson", (sample_0_dataframe, sample_1_dataframe))

def client_pearson_agg(client, list_list_precompute):
    return client.call("pearson_agg", list_list_precompute)

def client_skewness(client, sample_0_dataframe):
    return client.call("skewness", sample_0_dataframe)

def client_skewness_agg(client, list_list_precompute):
    return client.call("skewness_agg", list_list_precompute)

def client_variance(client, sample_0):
    return client.call("variance", sample_0)

def client_variance_agg(client, list_list_precompute):
    return client.call("variance_agg", list_list_precompute)

#user interface:

def fed_chi_square(clients, sample_0, sample_1):
    precompute = []
    for i, client in enumerate(clients):
        res = client_chi_square(client, sample_0[i], sample_1[i])
        precompute.append(res)
    return client_chi_square_agg(clients[0], precompute)

def fed_kolmogorov_smirnovdef(clients, sample_0, sample_ranked_0, distribution, count_total):
    precompute = []
    for i, client in enumerate(clients):
        res = client_kolmogorov_smirnovdef(client, sample_0[i], sample_1[i], distribution, count_total)
        precompute.append(res)
    return client_kolmogorov_smirnovdef_agg(clients[0], precompute)

def fed_kurtosis(clients, sample_0_dataframe):
    precompute = []
    for i, client in enumerate(clients):
        res = client_kurtosis(client, sample_0_dataframe[i])
        precompute.append(res)
    return client_kurtosis_agg(clients[0], precompute)

def fed_levene(clients, sample_0_series, sample_1_series, mean_0, mean_1):
    precompute = []
    for i, client in enumerate(clients):
        res = client_levene(client, sample_0_series[i], sample_1_series[i], mean_0[i], mean_1[i])
        precompute.append(res)
    return client_levene_agg(clients[0], precompute)

def fed_mann_whitney(clients, series_0, series_concatenated_ranked):
    precompute = []
    for i, client in enumerate(clients):
        res = client_mann_whitney(client, series_0[i], series_concatenated_ranked[i])
        precompute.append(res)
    return client_mann_whitney_agg(clients[0], precompute)

def fed_mean(clients, sample_0_dataframe):
    precompute = []
    for i, client in enumerate(clients):
        res = client_mean(client, sample_0_dataframe[i])
        precompute.append(res)
    return client_mean_agg(clients[0], precompute)

def fed_min_max(clients, series_sample):
    precompute = []
    for i, client in enumerate(clients):
        res = client_min_max(client, series_sample[i])
        precompute.append(res)
    return client_min_max_agg(clients[0], precompute)

def fed_paired_t(clients, sample_0_series, sample_1_series):
    precompute = []
    for i, client in enumerate(clients):
        res = client_paired_t(client, sample_0_series[i], sample_1_series[i])
        precompute.append(res)
    return client_paired_t_agg(clients[0], precompute)

def fed_pearson(clients, sample_0_dataframe, sample_1_dataframe):
    precompute = []
    for i, client in enumerate(clients):
        res = client_pearson(client, sample_0_dataframe[i], sample_1_dataframe[i])
        precompute.append(res)
    return client_pearson_agg(clients[0], precompute)

def fed_skewness(clients, sample_0_dataframe):
    precompute = []
    for i, client in enumerate(clients):
        res = client_skewness(client, sample_0_dataframe[i])
        precompute.append(res)
    return client_skewness_agg(clients[0], precompute)

def fed_unpaired_t(clients, sample_0_series, sample_1_series):
    precompute = []
    for i, client in enumerate(clients):
        res = client_unpaired_t(client, sample_0_series[i], sample_1_series[i])
        precompute.append(res)
    return client_unpaired_t_agg(clients[0], precompute)

def fed_variance(clients, sample_0):
    precompute = []
    for i, client in enumerate(clients):
        res = client_variance(client, sample_0[i])
        precompute.append(res)
    return client_variance_agg(clients[0], precompute)

def fed_wilcoxon_signed_rank(clients, sample_difference, sample_absolute_difference_ranked):
    precompute = []
    for i, client in enumerate(clients):
        res = client_wilcoxon_signed_rank(client, sample_difference[i], sample_absolute_difference_ranked[i])
        precompute.append(res)
    return client_wilcoxon_signed_rank_agg(clients[0], precompute)