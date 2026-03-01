
import pandas as pd
import osmnx as ox

def get_live_locality_score(lat, lon, radius_km=2):
    """
    Scans the area around a coordinate to generate model features.
    """
    # Fetch amenities from OpenStreetMap
    tags = {'amenity': ['school', 'hospital', 'police'], 'railway': 'station'}
    gdf = ox.features_from_point((lat, lon), tags=tags, dist=radius_km * 1000)
    
    # Feature Engineering for the XGBoost Model
    features = {
        'hospital_density': len(gdf[gdf['amenity'] == 'hospital']) if 'amenity' in gdf.columns else 0,
        'school_count': len(gdf[gdf['amenity'] == 'school']) if 'amenity' in gdf.columns else 0,
        'has_metro': 1 if 'railway' in gdf.columns else 0,
        'crime_safety_proxy': 100 - (len(gdf[gdf['amenity'] == 'police']) * 5) # Example proxy
    }
    return features
def get_proximity_features(lat, lon, radius=2000):
    """
    Calculates counts of amenities within a radius (in meters).
    """
    # Download points of interest (POIs) around the coordinate
    tags = {
        'amenity': ['school', 'hospital', 'university'],
        'railway': ['station'],
        'shop': ['mall', 'supermarket']
    }
    
    pois = ox.features_from_point((lat, lon), tags=tags, dist=radius)
    
    # Feature Vector
    features = {
        'school_count': len(pois[pois['amenity'] == 'school']) if 'amenity' in pois else 0,
        'hospital_count': len(pois[pois['amenity'] == 'hospital']) if 'amenity' in pois else 0,
        'metro_proximity': 1 if 'railway' in pois else 0, # Simple binary for MVP
        'mall_count': len(pois[pois['shop'] == 'mall']) if 'shop' in pois else 0
    }
    return features