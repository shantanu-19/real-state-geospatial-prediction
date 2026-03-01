import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import numpy as np
import time
import os

def add_geo_data():
    file_path = "india_housing_prices.csv"
    
    # Check if file exists first
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found in the current directory.")
        return

    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        print(f"Read {len(df)} rows. Starting geocoding...")

        # Unique Cities Geocoding
        unique_cities = df[['City', 'State']].drop_duplicates()
        unique_cities['full_addr'] = unique_cities['City'] + ", " + unique_cities['State'] + ", India"

        # Increased timeout to prevent the 'TimeoutError' you saw
        geolocator = Nominatim(user_agent="iit_bhuvneshwar_final", timeout=10)
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5, max_retries=3)

        lat_map, lon_map = {}, {}
        print(f"Geocoding {len(unique_cities)} unique cities... this will take ~1-2 minutes.")

        for addr in unique_cities['full_addr']:
            try:
                location = geocode(addr)
                if location:
                    lat_map[addr] = location.latitude
                    lon_map[addr] = location.longitude
                    print(f"✅ Found: {addr}")
                else:
                    lat_map[addr], lon_map[addr] = 20.5937, 78.9629 # India Center fallback
            except Exception as e:
                print(f"⚠️ Skipping {addr} due to connection issue: {e}")
                lat_map[addr], lon_map[addr] = 20.5937, 78.9629

        # Map and Jitter
        df['full_addr'] = df['City'] + ", " + df['State'] + ", India"
        df['Latitude'] = df['full_addr'].map(lat_map) + np.random.uniform(-0.04, 0.04, size=len(df))
        df['Longitude'] = df['full_addr'].map(lon_map) + np.random.uniform(-0.04, 0.04, size=len(df))

        df.drop(columns=['full_addr'], inplace=True)
        
        # Save to a NEW file first to avoid permission issues, then rename
        temp_file = "india_housing_prices_updated.csv"
        df.to_csv(temp_file, index=False)
        
        # Clean up: Rename temp to original
        os.remove(file_path)
        os.rename(temp_file, file_path)
        print("✅ SUCCESS: Latitude and Longitude added successfully!")

    except PermissionError:
        print("❌ CRITICAL ERROR: Permission Denied. PLEASE CLOSE EXCEL and stop the Streamlit app before running this script.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_geo_data()