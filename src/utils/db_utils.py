import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def upload_to_mysql(dataframe):
    """Takes a pandas dataframe and uploads it to property_listings table."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password="Tanu**123", # Your verified password
            database="real_estate"
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO property_listings 
        (price_total, area_sqft, bhk_count, locality_name, city, location) 
        VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
        """

        for _, row in dataframe.iterrows():
            # Generate a random/dummy coordinate if scraper doesn't provide lat/long
            # Or use a Geocoding API to turn locality_name into coordinates
            point_wkt = f"POINT({row['longitude']} {row['latitude']})"
            
            values = (
                row['price_total'], row['area_sqft'], row['bhk_count'],
                row['locality_name'], row['city'], point_wkt
            )
            cursor.execute(insert_query, values)

        conn.commit()
        print(f"✅ Successfully uploaded {len(dataframe)} rows.")
        conn.close()
    except Exception as e:
        print(f"❌ DB Upload Error: {e}")