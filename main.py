import pandas as pd
from src.utils.geocoder import GeoLocationService
from src.utils.db_utils import upload_to_mysql

def run_data_collection():
    # 1. Simulate Scraped Data (Replace with your Scraper output)
    raw_data = [
        {'price_total': 95.0, 'area_sqft': 1100, 'bhk_count': 2, 'locality_name': 'Powai', 'city': 'Mumbai'},
        {'price_total': 150.0, 'area_sqft': 1600, 'bhk_count': 3, 'locality_name': 'Worli', 'city': 'Mumbai'}
    ]
    df = pd.DataFrame(raw_data)
    
    # 2. Add Coordinates
    geo = GeoLocationService()
    lats, lons = [], []
    
    print("🌍 Starting Geocoding...")
    for _, row in df.iterrows():
        lat, lon = geo.get_coordinates(row['locality_name'], row['city'])
        lats.append(lat)
        lons.append(lon)
        time.sleep(1) # Respect Nominatim's usage policy (1 request/sec)
        
    df['latitude'] = lats
    df['longitude'] = lons
    
    # Filter out rows that couldn't be geocoded
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # 3. Upload to MySQL
    print("💾 Uploading to Database...")
    upload_to_mysql(df)

if __name__ == "__main__":
    run_data_collection()