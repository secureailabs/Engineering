import os
import time

from zero import ZeroClient

scn_names = os.getenv("SCN_NAMES").split(",")

print(scn_names)

clients = []
rdfs = []
rdf_itr = 1
for scn_name in scn_names:
    print(f"Allocating client {scn_name}")
    new_client = ZeroClient(scn_name, 5556)
    clients.append(new_client)
    rdfs.append(new_client.call("load_df_from_csv", f"/data/kidney_clean_{rdf_itr}.csv"))
    rdf_itr = rdf_itr + 1
    print(f"Got client {rdf_itr}")

itr = 0
while True:
    print(f"Iteration {itr}")
    means = []
    min_maxes = []
    # Iterate through our clients to load aggregates
    for client, df in zip(clients, rdfs):
        means.append(client.call("mean", df["age"]))
        min_maxes.append(client.call("min_max", df["age"]))

    agg_mean = clients[0].call("mean_agg", means)
    agg_min_max = clients[1].call("min_max_agg", min_maxes)

    assert agg_mean == 51.353125
    assert agg_min_max == (-1.30625, 91.80625)
    itr = itr + 1
