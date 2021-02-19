
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

df_daily = pd.read_gbq("select * from `intense-arbor-186802`.sample_data.daily_data",
                 project_id="intense-arbor-186802")

top_6_most_used_product = list(df_daily.groupby(["product"]).size().sort_values(ascending=False)[:6].index)

df_daily_6 = df_daily[df_daily["product"].isin(top_6_most_used_product)]

# df_daily_6 = df_daily_6.set_index(["start_time"])

# df_daily_6.groupby(["start_time","product"])["cost"].plot()

df_daily_6["usage_amount_norm"] = (df_daily_6["usage_amount"] -
                                   df_daily_6["usage_amount"].min()) / (df_daily_6["usage_amount"].max() -
                                                                        df_daily_6["usage_amount"].min())

df_daily_6["cost_norm"] = (df_daily_6["cost"] -
                                   df_daily_6["cost"].min()) / (df_daily_6["cost"].max() -
                                                                        df_daily_6["cost"].min())

df_daily_5 = df_daily_6[~df_daily_6["product"].isin(["Cloud Storage","Cloud DNS","Cloud SQL"])]

df_daily_5.groupby(["start_time", "product"]).min()["cost_norm"].unstack().plot()