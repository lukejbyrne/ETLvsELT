# ETL Example
# Extract, Transform, Load

import requests
import pandas as pd
import os

# Step 1: Extract
# Fetch raw data from an API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-12-01&endtime=2023-12-02"
response = requests.get(url)
data = response.json()["features"]

# Step 2: Transform
# Transform data in Python
transformed_data = []
for event in data:
    coords = event["geometry"]["coordinates"]
    properties = event["properties"]
    transformed_data.append({
        "id": event["id"],
        "longitude": coords[0],
        "latitude": coords[1],
        "magnitude": properties.get("mag"),
        "place": properties.get("place"),
    })

df = pd.DataFrame(transformed_data)

# Clean missing values
df.fillna({"magnitude": 0, "place": "Unknown"}, inplace=True)

# Step 3: Load
# Save transformed data directly to Final Dataset
output_path = "final/etl/earthquake_data_final.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"ETL Process Complete: Data saved to {output_path}")