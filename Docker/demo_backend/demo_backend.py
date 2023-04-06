"""
For temporary demo purpose
Apr. 5
"""

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

df1 = pd.read_csv("data_frame_0.csv")
df2 = pd.read_csv("data_frame_1.csv")
df = pd.concat([df1, df2])

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/demo/test")
async def test() -> dict:
    return {"status": True, "data": "Hello World", "message": "Test passed"}

@app.post("/demo/paired_t")
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
            if cohort["filter_operator"][i - 1] == "and":
                prev_df = prev_df & tmp_df
            elif cohort["filter_operator"][i - 1] == "or":
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
