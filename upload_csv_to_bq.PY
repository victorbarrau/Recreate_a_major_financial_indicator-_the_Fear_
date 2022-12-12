import pandas as pd
# from pandas.io import gbq
import os
import numpy as np
import pandas_gbq
from google.cloud import bigquery

dept_dt=pd.read_csv('data_trends.csv')
#print(dept_dt)

# Replace with Project Id
project = 'sublime-vial-365809'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./cred.json"

pandas_gbq.to_gbq(dept_dt, destination_table='Data_trends.Trends', project_id='sublime-vial-365809',if_exists='fail')



job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    schema=[
        # Specify the type of columns whose type cannot be auto-detected. For
        # example the "title" column uses pandas dtype "object", so its
        # data type is ambiguous.
        bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.DATE), 
        # Indexes are written if included in the schema by name.
        bigquery.SchemaField("bitcoin", bigquery.enums.SqlTypeNames.STRING),
    ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
)
client = bigquery.Client()
table_id = "Data_trends.Trends"
job = client.load_table_from_dataframe(
    dept_dt, table_id, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)