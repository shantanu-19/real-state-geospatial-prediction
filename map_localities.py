import pandas as pd
import numpy as np

def apply_real_names():
    file_path = "india_housing_prices.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    # Real-world locality dictionary for major cities
    city_mapping = {
        'Bangalore': ['Whitefield', 'Electronic City', 'Indiranagar', 'Koramangala', 'HSR Layout', 'Hebbal', 'Yelahanka', 'Marathahalli'],
        'Mumbai': ['Andheri West', 'Bandra West', 'Powai', 'Worli', 'Juhu', 'Borivali East', 'Dadar', 'Ghatkopar'],
        'Delhi': ['Dwarka', 'Rohini', 'Saket', 'Vasant Kunj', 'Janakpuri', 'Lajpat Nagar', 'Karol Bagh', 'Connaught Place'],
        'Pune': ['Hinjewadi', 'Baner', 'Wakad', 'Kothrud', 'Viman Nagar', 'Hadapsar', 'Kharadi', 'Magarpatta'],
        'Chennai': ['Adyar', 'Velachery', 'Anna Nagar', 'T. Nagar', 'OMR', 'Mylapore', 'Besant Nagar', 'Guindy'],
        'Hyderabad': ['Gachibowli', 'HITEC City', 'Jubilee Hills', 'Banjara Hills', 'Kondapur', 'Madhapur', 'Kukatpally'],
        'Jaipur': ['Malviya Nagar', 'Vaishali Nagar', 'Mansarovar', 'Jagatpura', 'C-Scheme', 'Bani Park', 'Raja Park'],
        'Lucknow': ['Gomti Nagar', 'Aliganj', 'Indira Nagar', 'Hazratganj', 'Mahanagar', 'Ashiyana', 'Jankipuram'],
        'Kolkata': ['Salt Lake', 'New Town', 'Ballygunge', 'Tollygunge', 'Behala', 'Park Street', 'Dum Dum'],
        'Ahmedabad': ['Satellite', 'Prahlad Nagar', 'Bopal', 'Bodakdev', 'Maninagar', 'Vastrapur', 'Chandkheda'],
        'Gurgaon': ['DLF Phase 5', 'Sushant Lok', 'Sector 56', 'Golf Course Road', 'Sohna Road', 'Sector 45'],
        'Noida': ['Sector 62', 'Sector 15', 'Sector 137', 'Sector 18', 'Sector 50', 'Sector 76']
    }

    print("Mapping anonymized IDs to real Indian neighborhoods...")
    
    unique_cities = df['City'].unique()
    for city in unique_cities:
        # Get unique Locality IDs for this city
        city_loc_ids = df[df['City'] == city]['Locality'].unique()
        
        # Get real names for this city (or generic names if not in dict)
        real_names = city_mapping.get(city, [f"{city} Sector {i+1}" for i in range(len(city_loc_ids))])
        
        # If we have more Locality IDs than real names, repeat/cycle the real names
        if len(real_names) < len(city_loc_ids):
            real_names = (real_names * (len(city_loc_ids) // len(real_names) + 1))[:len(city_loc_ids)]
        
        # Create a tiny mapping for this city
        city_map = dict(zip(city_loc_ids, real_names))
        
        # Apply only to rows of this city
        mask = df['City'] == city
        df.loc[mask, 'Locality'] = df.loc[mask, 'Locality'].map(city_map)

    df.to_csv(file_path, index=False)
    print("✅ SUCCESS: Locality names updated to real-world neighborhoods!")

if __name__ == "__main__":
    apply_real_names()