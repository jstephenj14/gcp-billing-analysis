import os
import pandas as pd
pd.set_option('display.max_columns', None)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/jstep/Downloads/intense-arbor-186802-107ac532385b.json"

from google.cloud import bigquery

df = pd.read_gbq("select * from `intense-arbor-186802`.sample_data.gcp_billing_sample",
                 project_id="intense-arbor-186802")


df["project"].iloc[0]["name"]

df["project_name"] = df.apply(lambda row: row["project"]["name"], axis =1)