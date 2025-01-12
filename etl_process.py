import json
import requests
from datetime import date, timedelta
import pandas as pd
from geopy.geocoders import Nominatim

# Set paths
bronze_adls = "containers/bronze/"
silver_adls = "containers/silver/"
gold_adls = "containers/gold/"

# ETL Process

# Extract: Fetch data from API
start_date = (date.today() - timedelta(1)).isoformat()
end_date = date.today().isoformat()

url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json().get('features', [])

    if not data:
        print("No data returned for the specified date range.")
    else:
        file_path = f"{bronze_adls}/{start_date}_earthquake_data.json"
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")

# Transform: Process and validate the data
with open(f"{bronze_adls}/{start_date}_earthquake_data.json", 'r') as f:
    earthquake_data = json.load(f)

df = pd.json_normalize(
    earthquake_data,
    record_path=['geometry', 'coordinates'],
    meta=['id'],
    errors='ignore'
)

df.columns = ['longitude', 'latitude', 'elevation', 'id']
df['longitude'] = df['longitude'].fillna(0)
df['latitude'] = df['latitude'].fillna(0)

if 'properties.time' in df:
    df['time'] = pd.to_datetime(df['properties.time'], unit='ms')

# Save intermediate data to Silver
df.to_csv(f"{silver_adls}/earthquake_events_silver.csv", index=False)

# Further transformations: Add geolocation and classification
geolocator = Nominatim(user_agent="geoapi")

def get_country_code(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en')
        return location.raw.get('address', {}).get('country_code', 'unknown').upper()
    except Exception as e:
        print(f"Error reverse geocoding {lat}, {lon}: {e}")
        return 'unknown'

df['country_code'] = df.apply(lambda row: get_country_code(row['latitude'], row['longitude']), axis=1)

df['sig_class'] = pd.cut(
    df['sig'],
    bins=[-float('inf'), 100, 500, float('inf')],
    labels=['Low', 'Moderate', 'High']
)

# Load: Save transformed data to Gold
df.to_csv(f"{gold_adls}/earthquake_events_gold.csv", index=False)
print("ETL process complete.")
