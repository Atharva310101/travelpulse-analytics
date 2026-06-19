import os
import pandas as pd
from google.cloud import bigquery

# Path to your service account key
KEY_PATH = "bigquery_key.json"

if not os.path.exists(KEY_PATH):
    raise FileNotFoundError(
        f"Credentials file '{KEY_PATH}' not found in the root directory. "
        "Please ensure you copied and renamed your JSON key correctly."
    )

# Clean, standard authentication method
client = bigquery.Client.from_service_account_json(KEY_PATH)

# Define dataset name using the verified project ID
DATASET_ID = f"{client.project}.raw_travelpulse"

# 1. Create the Dataset if it does not exist
dataset = bigquery.Dataset(DATASET_ID)
dataset.location = "US"  # You can change this to your preferred region (e.g., EU)

try:
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset '{DATASET_ID}' verified/created in {dataset.location}.")
except Exception as e:
    print(f"Error creating dataset: {e}")
    exit(1)

# 2. Map CSV files to target table names
csv_tables = {
    "data/dim_airports.csv": "dim_airports",
    "data/dim_airlines.csv": "dim_airlines",
    "data/dim_corporate_clients.csv": "dim_corporate_clients",
    "data/fact_bookings.csv": "fact_bookings"
}

# 3. Load CSV data into BigQuery
for file_path, table_name in csv_tables.items():
    if not os.path.exists(file_path):
        print(f"Warning: File '{file_path}' not found. Skipping...")
        continue
        
    print(f"Uploading '{file_path}' to table '{table_name}'...")
    
    # Read CSV with pandas to handle formatting cleanly
    df = pd.read_csv(file_path)
    
    # Set up BigQuery table path
    table_ref = client.dataset("raw_travelpulse").table(table_name)
    
    # Configure load job
    # WRITE_TRUNCATE ensures that running this script multiple times overwrites the table 
    # instead of appending duplicates.
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,  # Automatically infer column data types
    )
    
    try:
        # Perform the upload
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Wait for the load job to complete
        
        # Verify row counts
        destination_table = client.get_table(table_ref)
        print(f" Successfully loaded {destination_table.num_rows} rows into '{table_name}'.")
    except Exception as e:
        print(f"❌ Failed to load '{table_name}': {e}")

print("\nAll available tables successfully ingested into BigQuery!")