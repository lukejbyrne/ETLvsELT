import json
import requests
from datetime import date, timedelta
import pandas as pd
from geopy.geocoders import Nominatim

# Set paths
bronze_adls = "containers/bronze/"
silver_adls = "containers/silver/"
gold_adls = "containers/gold/"

# ELT Process

# Extract: Fetch data from API and save raw data to Bronze
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

# Load: Save raw data to Silver
with open(f"{bronze_adls}/{start_date}_earthquake_data.json", 'r') as f:
    earthquake_data = json.load(f)

df = pd.json_normalize(
    earthquake_data,
    record_path=['geometry', 'coordinates'],
    meta=['id'],
    errors='ignore'
)

df.columns = ['longitude', 'latitude', 'elevation', 'id']
df.to_csv(f"{silver_adls}/earthquake_events_silver.csv", index=False)

# Transform: Process and enrich data in Gold
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

df.to_csv(f"{gold_adls}/earthquake_events_gold.csv", index=False)
print("ELT process complete.")
