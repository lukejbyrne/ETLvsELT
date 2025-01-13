# ELT Example
# Extract, Load, Transform

import requests
import pandas as pd
import os
import json

# Step 1: Extract
# Fetch raw data from an API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-12-01&endtime=2023-12-02"
response = requests.get(url)
data = response.json()["features"]

# Step 2: Load
# Save raw data to Raw Dataset
raw_path = "elt/raw/earthquake_data_raw.json"
os.makedirs(os.path.dirname(raw_path), exist_ok=True)
with open(raw_path, "w") as f:
    json.dump(data, f)
print(f"Raw data saved to {raw_path}")

# Step 3: Transform
# Load raw JSON data
with open(raw_path, "r") as f:
    raw_data = json.load(f)

# Extract relevant fields
transformed_data = []
for event in raw_data:
    geometry = event["geometry"]
    properties = event["properties"]
    transformed_data.append({
        "id": event["id"],
        "longitude": geometry["coordinates"][0],
        "latitude": geometry["coordinates"][1],
        "magnitude": properties.get("mag", 0),
        "place": properties.get("place", "Unknown"),
    })

# Create DataFrame
df = pd.DataFrame(transformed_data)

# Save to Final Dataset
output_path = "final/elt/earthquake_data_final.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"ELT Process Complete: Data saved to {output_path}")
