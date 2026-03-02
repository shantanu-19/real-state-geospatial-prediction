import streamlit as st
import pandas as pd
import folium
import numpy as np
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Dashboard Configuration
st.set_page_config(page_title="Real Estate Investment AI", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("india_housing_prices.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.sidebar.header("📊 Global Filters")
    all_states = sorted(df['State'].unique())
    selected_state = st.sidebar.selectbox("State", all_states)
    
    filtered_df = df[df['State'] == selected_state]
    all_cities = sorted(filtered_df['City'].unique())
    selected_city = st.sidebar.selectbox("City", all_cities)

    tab1, tab2, tab3 = st.tabs(["🎯 AI Price & Investment Engine", "🗺️ Geospatial Analysis", "📈 Market Analytics"])

    # --- TAB 1: PREDICTION & INVESTMENT ---
    with tab1:
        st.subheader("Property Value & Investment Projection")
        
        with st.expander("ℹ️ How the Investment Score Works", expanded=False):
            st.write("Our model analyzes proximity to metro, school quality, and future infrastructure to calculate a 'Deal Score' and 5-year ROI.")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🏠 Property Basics")
            localities = sorted(filtered_df[filtered_df['City'] == selected_city]['Locality'].unique())
            locality = st.selectbox("Locality", localities)
            prop_type = st.selectbox("Property Type", sorted(df['Property_Type'].unique()))
            furnished = st.selectbox("Furnished Status", sorted(df['Furnished_Status'].unique()))
            availability = st.selectbox("Availability Status", sorted(df['Availability_Status'].unique()))
            
        with col2:
            st.markdown("### 📏 Dimensions & Age")
            area = st.number_input("Area (Sqft)", min_value=100, value=1200, step=100)
            bhk = st.slider("BHK", 1, 10, 2)
            age = st.slider("Property Age (Years)", 0, 50, 5)

        with col3:
            st.markdown("### 🏗️ Infrastructure Signals")
            metro_dist = st.slider("Distance to Metro (km)", 0.0, 10.0, 1.5)
            schools = st.slider("School Quality Rating", 1, 10, 7)
            infra_score = st.slider("Future Infra Score (Govt Projects)", 0.1, 1.0, 0.7)

        if st.button("Analyze Investment Potential", use_container_width=True):
            try:
                # Prepare data for prediction (Ensure CustomData handles the new features)
                data = CustomData(
                    area_sqft=area, bhk_count=bhk, age=age, 
                    locality_name=locality, city=selected_city, state=selected_state, 
                    property_type=prop_type, furnished_status=furnished,
                    availability_status=availability,
                    metro_proximity_km=metro_dist, # NEW
                    school_rating=schools,         # NEW
                    future_infra_score=infra_score # NEW
                )
                
                pred_df = data.get_data_as_data_frame()
                predict_pipeline = PredictPipeline()
                results = predict_pipeline.predict(pred_df)
                predicted_price = results[0]

                st.divider()
                
                # --- RESULTS SECTION ---
                res_col1, res_col2, res_col3 = st.columns(3)
                
                # 1. Price Result
                res_col1.metric("Estimated Market Value", f"₹{round(predicted_price, 2)} L")
                
                # 2. Deal Scorer Logic
                # Compare against average price in that locality
                avg_locality_price = filtered_df[filtered_df['Locality'] == locality]['Price_in_Lakhs'].mean()
                price_diff = ((predicted_price - avg_locality_price) / avg_locality_price) * 100
                
                if price_diff > 10:
                    res_col2.info("⚖️ Deal Status: Fairly Priced")
                elif price_diff < -5:
                    res_col2.success(f"💎 Deal Status: UNDERVALUED (Save ~{abs(round(price_diff))}% )")
                else:
                    res_col2.warning("⚠️ Deal Status: Premium Pricing")

                # 3. Rental Yield Calculator (Assuming 3% Avg)
                res_col3.metric("Est. Monthly Rent", f"₹{round((predicted_price * 0.03 / 12)*100000)} ")

                # --- INVESTMENT PROJECTION ---
                st.markdown("### 📈 5-Year Capital Appreciation Projection")
                # Simple CAGR model based on infra score (Higher infra score = higher appreciation)
                cagr = 0.06 + (infra_score * 0.05) # Base 6% + up to 5% bonus
                
                years = [1, 3, 5]
                projections = [predicted_price * (1 + cagr)**y for y in years]
                
                proj_df = pd.DataFrame({
                    'Timeline': ['1 Year', '3 Years', '5 Years'],
                    'Estimated Value (Lakhs)': projections
                })
                st.line_chart(proj_df.set_index('Timeline'))
                
                st.balloons()
            except Exception as e:
                st.error(f"Analysis Error: {e}. Ensure predict_pipeline.py is updated with new features.")

    # --- TAB 2: GEOSPATIAL MAP ---
    with tab2:
        st.subheader(f"📍 Market Heatmap: {selected_city}")
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            city_map_df = df[df['City'] == selected_city].dropna(subset=['Latitude', 'Longitude'])
            if not city_map_df.empty:
                start_lat, start_lon = city_map_df['Latitude'].mean(), city_map_df['Longitude'].mean()
                m = folium.Map(location=[start_lat, start_lon], zoom_start=12, tiles="cartodbpositron")
                heat_data = city_map_df[['Latitude', 'Longitude', 'Price_in_Lakhs']].values.tolist()
                HeatMap(heat_data, radius=15, blur=10).add_to(m)
                st_folium(m, width=1200, height=500)
            else:
                st.warning("No coordinate data available for this city.")

    # --- TAB 3: ANALYTICS ---
    with tab3:
        st.subheader(f"Historical Trends & Market Distribution")
        col_a, col_b = st.columns(2)
        if not filtered_df.empty:
            with col_a:
                st.write("Price Distribution by BHK")
                bhk_chart = filtered_df.groupby('BHK')['Price_in_Lakhs'].mean()
                st.bar_chart(bhk_chart)
            with col_b:
                st.write("Availability Status Impact")
                avail_chart = filtered_df.groupby('Availability_Status')['Price_in_Lakhs'].mean()
                st.bar_chart(avail_chart)

else:
    st.error("Data file missing. Please ensure 'india_housing_prices.csv' is present.")