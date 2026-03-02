import pandas as pd
import numpy as np

def fix_data_logic():
    df = pd.read_csv("india_housing_prices.csv")
    df.columns = df.columns.str.strip()
    
    # 1. Macro-Economics: City & Locality Tiers
    city_rates = {city: np.random.uniform(0.08, 0.30) for city in df['City'].unique()}
    prop_multipliers = {'Villa': 1.6, 'Independent House': 1.3, 'Apartment': 1.0}
    
    # 2. FEATURE ENGINEERING: NEW INVESTMENT SIGNALS
   
    df['metro_proximity_km'] = np.random.uniform(0.2, 5.0, len(df))
    df['school_rating'] = np.random.randint(1, 11, len(df))
    df['crime_rate_index'] = np.random.uniform(0.01, 0.08, len(df))
    df['future_infra_score'] = np.random.uniform(0.5, 1.0, len(df)) # Upcoming projects impact

    # 3. REALISTIC PRICE CALCULATION 
    def calculate_investment_price(row):
        # Base Price from Size and City
        base = row['Size_in_SqFt'] * city_rates.get(row['City'], 0.1)
        
        # Impact of Amenities & Infrastructure
        infra_impact = (row['future_infra_score'] * 20)  # Future projects boost price
        metro_impact = (5 - row['metro_proximity_km']) * 3 # Closer to metro = higher price
        safety_impact = (1 - row['crime_rate_index']) * 10
        
        # Final weighted price
        total = (base * prop_multipliers.get(row['Property_Type'], 1.0)) 
        total += infra_impact + metro_impact + safety_impact + (row['BHK'] * 12)
        
        # Adding 5% natural market noise
        noise = np.random.normal(1, 0.05)
        return round(total * noise, 2)

    print("Injecting Investment Signals and Infrastructure data...")
    df['Price_in_Lakhs'] = df.apply(calculate_investment_price, axis=1)
    
    # 4. RENTAL YIELD & INVESTMENT PROJECTION (Financial Metrics)
    # Average Indian rental yield is 2.5% - 4%
    df['annual_rental_income'] = df['Price_in_Lakhs'] * np.random.uniform(0.025, 0.04)
    df['price_appreciation_5yr'] = df['Price_in_Lakhs'] * (1.08 ** 5) # Assuming 8% CAGR
    
    # Update PSF
    df['Price_per_SqFt'] = df['Price_in_Lakhs'] / df['Size_in_SqFt']
    
    df.to_csv("india_housing_prices.csv", index=False)
    print("✅ SUCCESS: Data is now a complete Investment Dataset!")

if __name__ == "__main__":
    fix_data_logic()