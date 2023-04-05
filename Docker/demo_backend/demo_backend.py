"""
For temporary demo purpose
Apr. 5
"""

import pandas as pd
from fastapi import FastAPI

df1 = pd.read_csv("")
df2 = pd.read_csv("")
df = pd.concat([df1, df2])

app = FastAPI()


@app.get("/demo/paired_t")
async def paired_t(cohort: dict, analysis: dict) -> dict:

    i = 0
    prev_df = pd.DataFrame()
    for item in cohort["filter"]:
        tmp_df = pd.DataFrame()
        if item["operator"] == "eq":
            tmp_df = df[item["series_name"]] == item["value"]
        elif item["operator"] == "gt":
            tmp_df = df[item["series_name"]] > item["value"]
        elif item["operator"] == "lt":
            tmp_df = df[item["series_name"]] < item["value"]
        else:
            raise Exception("Operator not supported")
        if i >= 1:
            if cohort["filter_operator"][i - 1] == "AND":
                prev_df = prev_df & tmp_df
            elif cohort["filter_operator"][i - 1] == "OR":
                prev_df = prev_df | tmp_df
            else:
                raise Exception("filter operator not supported")
        else:
            prev_df = tmp_df
        i += 1

    res_df = df[prev_df]

    from scipy.stats import ttest_ind

    stat, pvalue = ttest_ind(
        res_df[analysis["parameter"]["series_name_0"]], res_df[analysis["parameter"]["series_name_1"]]
    )

    return {
        "status": True,
        "data": {
            "statistic": str(stat),
            "pvalue": str(pvalue),
        },
        "message": "Result computed successfully",
    }
