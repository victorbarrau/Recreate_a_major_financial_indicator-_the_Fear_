from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
import datetime
import io
import numpy as np
import pandas_gbq


client = storage.Client()
bucket = client.get_bucket('data-coin-market-cap')
crypto_list = ["bnb","eth","bnb","doge"]
for crypto in crypto_list :
    now = datetime.datetime.now()
    
    date=now.strftime("%Y%m%d")
    file_name = crypto+"/dominance_du_"+ date +".csv"
    blob = bucket.get_blob(file_name)
    content = blob.download_as_string()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    df['date'] = pd.to_datetime(date, format='%Y-%m-%d')
    project = 'sublime-vial-365809'
    destination_table = 'dominance.'+crypto



    job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.DATE), 
            bigquery.SchemaField("symbol", bigquery.enums.SqlTypeNames.STRING), 
            # Indexes are written if included in the schema by name.
            bigquery.SchemaField("dominance", bigquery.enums.SqlTypeNames.FLOAT),
            
        ],
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        write_disposition="WRITE_APPEND",
    )
    client = bigquery.Client()
    table_id = "dominance."+crypto
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
)
