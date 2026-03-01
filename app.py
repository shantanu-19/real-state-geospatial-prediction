import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Dashboard Configuration
st.set_page_config(page_title="Real Estate Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("india_housing_prices.csv")
        # Standardize column names: remove hidden spaces
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("📊 Global Filters")
    
    all_states = sorted(df['State'].unique()) if 'State' in df.columns else []
    selected_state = st.sidebar.selectbox("State", all_states)
    
    filtered_df = df[df['State'] == selected_state]
    all_cities = sorted(filtered_df['City'].unique()) if 'City' in df.columns else []
    selected_city = st.sidebar.selectbox("City", all_cities)

    # Tabs for Dashboard
    tab1, tab2, tab3 = st.tabs(["🎯 Price Prediction", "🗺️ Market Heatmap", "📈 Analytics"])

    # --- TAB 1: PREDICTION ---
    with tab1:
        st.subheader("Property Value Estimator")
        col1, col2 = st.columns(2)
        
        with col1:
            localities = sorted(filtered_df[filtered_df['City'] == selected_city]['Locality'].unique()) if 'Locality' in df.columns else ["Locality_1"]
            locality = st.selectbox("Locality", localities)
            
            prop_types = sorted(df['Property_Type'].unique()) if 'Property_Type' in df.columns else ["Apartment"]
            prop_type = st.selectbox("Property Type", prop_types)
            
            furnished_list = sorted(df['Furnished_Status'].unique()) if 'Furnished_Status' in df.columns else ["Unfurnished"]
            furnished = st.selectbox("Furnished Status", furnished_list)

            # ADDED: Availability Status dropdown for the 10th column
            avail_list = sorted(df['Availability_Status'].unique()) if 'Availability_Status' in df.columns else ["Ready to Move"]
            availability = st.selectbox("Availability Status", avail_list)
            
        with col2:
            area = st.number_input("Area (Sqft)", min_value=100, value=1200, step=100)
            bhk = st.slider("BHK", 1, 10, 2)
            age = st.slider("Property Age (Years)", 0, 50, 5)

        if st.button("Calculate Market Value"):
            try:
                # CustomData matches the 10-column structure
                data = CustomData(
                    area_sqft=area, 
                    bhk_count=bhk, 
                    age=age, 
                    locality_name=locality, 
                    city=selected_city, 
                    state=selected_state, 
                    property_type=prop_type, 
                    furnished_status=furnished,
                    availability_status=availability
                )
                
                pred_df = data.get_data_as_data_frame()
                
                predict_pipeline = PredictPipeline()
                results = predict_pipeline.predict(pred_df)
                
                # Display Prediction result
                st.metric(label="Estimated Market Value", value=f"₹{round(results[0], 2)} Lakhs")
                st.balloons()
            except Exception as e:
                st.error(f"Prediction Error: {e}")

    # --- TAB 2: GEOSPATIAL MAP ---
    with tab2:
        st.subheader(f"📍 Real Estate Price Heatmap: {selected_city}")
        
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            city_map_df = df[df['City'] == selected_city].dropna(subset=['Latitude', 'Longitude'])
            
            if not city_map_df.empty:
                start_lat = city_map_df['Latitude'].mean()
                start_lon = city_map_df['Longitude'].mean()
                
                m = folium.Map(location=[start_lat, start_lon], zoom_start=12, tiles="cartodbpositron")
                
                # prepare heatmap data
                heat_data = city_map_df[['Latitude', 'Longitude', 'Price_in_Lakhs']].values.tolist()
                HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)
                
                st_folium(m, width=1200, height=600)
            else:
                st.warning(f"No coordinate data found for {selected_city}.")
        else:
            st.error("⚠️ Coordinates Not Found! Please run 'python add_coordinates.py' first.")

    # --- TAB 3: ANALYTICS ---
    with tab3:
        st.subheader(f"Market Trends in {selected_state}")
        col_a, col_b = st.columns(2)
        
        if not filtered_df.empty:
            with col_a:
                st.write("Average Price by Property Type")
                chart_data = filtered_df.groupby('Property_Type')['Price_in_Lakhs'].mean()
                st.bar_chart(chart_data)
                
            with col_b:
                st.write("Price vs Area Trend (Sample Data)")
                sample_size = min(len(filtered_df), 1000)
                st.scatter_chart(filtered_df[['Size_in_SqFt', 'Price_in_Lakhs']].sample(sample_size))
        else:
            st.info("No data available for the selected filters.")
else:
    st.error("Could not load data. Check if 'india_housing_prices.csv' is in the root folder.")