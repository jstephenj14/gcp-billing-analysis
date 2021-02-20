
import os
import pandas as pd
pd.set_option('display.max_columns', None)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/jstep/Downloads/intense-arbor-186802-107ac532385b.json"

from google.cloud import bigquery

# df = pd.read_gbq("select * from `intense-arbor-186802`.sample_data.gcp_billing_sample",
#                  project_id="intense-arbor-186802")
#
# df["start_time"] = pd.to_datetime(df["start_time"])
# df["end_time"] = pd.to_datetime(df["end_time"])
#
# df.memory_usage(deep=True).sum()

import numpy as np

df_daily = pd.read_gbq("select * from `intense-arbor-186802`.sample_data.top_3_prods",
                 project_id="intense-arbor-186802")

top_6_most_used_product = list(df_daily.groupby(["product"]).size().sort_values(ascending=False)[:6].index)

df_daily_6 = df_daily[df_daily["product"].isin(top_6_most_used_product)]

# Trying to plot topo 6
df_daily_6["usage_amount_norm"] = (df_daily_6["usage_amount"] -
                                   df_daily_6["usage_amount"].min()) / (df_daily_6["usage_amount"].max() -
                                                                        df_daily_6["usage_amount"].min())

df_daily_6["cost_norm"] = (df_daily_6["cost"] -
                                   df_daily_6["cost"].min()) / (df_daily_6["cost"].max() -
                                                                        df_daily_6["cost"].min())

df_daily_5 = df_daily_6[~df_daily_6["product"].isin(["Cloud Storage","Cloud DNS","Cloud SQL"])]

df_daily_5.groupby(["start_time", "product"]).min()["cost_norm"].unstack().plot()

#
def plot_prod(product):
    df_daily_cloudSQL = df_daily[df_daily["product"] == product]
    df_daily_cloudSQL = df_daily_cloudSQL[["start_time","unit","cost"]]

    df_daily_cloudSQL_pivot = pd.pivot_table(df_daily_cloudSQL, values="cost", index="start_time", columns="unit")

    for col in df_daily_cloudSQL_pivot.columns:
        df_daily_cloudSQL_pivot[col] = np.log(df_daily_cloudSQL_pivot[col])

    df_daily_cloudSQL_pivot.plot(title=product)

plot_prod("BigQuery")
plot_prod("Cloud Storage")
plot_prod("Compute Engine")

df_daily_cloudSQL = df_daily[df_daily["product"] == "BigQuery"]
df_daily_cloudSQL = df_daily_cloudSQL[["start_time", "unit", "cost"]]

df_daily_cloudSQL_pivot = pd.pivot_table(df_daily_cloudSQL, values="cost", index="start_time", columns="unit")


df_daily_cloudSQL_pivot["byte-seconds"] = np.log(df_daily_cloudSQL_pivot["byte-seconds"] )
df_daily_cloudSQL_pivot["bytes"] = np.log(df_daily_cloudSQL_pivot["bytes"] )

df_daily_cloudSQL_pivot.plot(title="BigQuery")