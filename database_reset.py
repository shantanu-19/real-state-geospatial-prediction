import pandas as pd
from sqlalchemy import create_engine

def reset_and_upload():
    try:
        # Use your verified credentials
        engine = create_engine("mysql+mysqlconnector://root:Tanu**123@localhost/real_estate")
        csv_path = r"D:\New folder\IIT BHUVNESHWAR PROJECTS\real-estate-geospatial-prediction\india_housing_prices.csv"
        
        df = pd.read_csv(csv_path)
        
        # MAPPING ALL KEY SIGNAL COLUMNS
        mapping = {
            'Price_in_Lakhs': 'price_total',
            'Size_in_SqFt': 'area_sqft',
            'BHK': 'bhk_count',
            'Locality': 'locality_name',
            'City': 'city',
            'State': 'state',
            'Property_Type': 'property_type',
            'Furnished_Status': 'furnished_status',
            'Age_of_Property': 'age',
            'Availability_Status': 'availability_status' # ADDED THIS
        }
        
        df = df.rename(columns=mapping)
        
        # SELECT ALL 10 COLUMNS FOR HIGH ACCURACY
        required_columns = [
            'price_total', 'area_sqft', 'bhk_count', 'age', 
            'locality_name', 'city', 'state', 'property_type', 
            'furnished_status', 'availability_status'
        ]
        
        final_df = df[required_columns].dropna()

        # Overwrite the table with the new column
        final_df.to_sql('property_listings', con=engine, if_exists='replace', index=False)
        print("✅ SUCCESS: Database reset with 10 High-Signal columns!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    reset_and_upload()