from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import time
from src.utils.logger import logging

class GeoLocationService:
    def __init__(self):
        # user_agent is required; use your project name
        self.geolocator = Nominatim(user_agent="real_estate_analyzer")

    def get_coordinates(self, locality, city):
        """Converts address string to (Latitude, Longitude)"""
        try:
            address = f"{locality}, {city}, India"
            location = self.geolocator.geocode(address)
            
            if location:
                logging.info(f"Geocoded: {address} to {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
            
            logging.warning(f"Could not find coordinates for: {address}")
            return None, None
            
        except GeopyError as e:
            logging.error(f"Geocoding error: {e}")
            return None, None