import time

from zero import ZeroClient

clients = [ZeroClient("scn_kidney_clean_1", 5556), ZeroClient("scn_kidney_clean_2", 5556)]

rdf1 = clients[0].call("load_df_from_csv", "/data/kidney_clean_1.csv")
rdf2 = clients[1].call("load_df_from_csv", "/data/kidney_clean_2.csv")


itr = 0
while True:
    print(f"Iteration {itr}")
    means = [clients[0].call("mean", rdf1["age"]), clients[1].call("mean", rdf2["age"])]
    agg_mean = clients[0].call("mean_agg", means)

    min_maxes = [clients[0].call("min_max", rdf1["age"]), clients[1].call("min_max", rdf2["age"])]
    agg_min_max = clients[1].call("min_max_agg", min_maxes)

    assert agg_mean == 51.353125
    assert agg_min_max == (-1.30625, 91.80625)
    itr = itr + 1
