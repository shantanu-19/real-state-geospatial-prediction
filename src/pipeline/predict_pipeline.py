import os
import sys
import pandas as pd
from src.utils.exception import CustomException
from src.utils.main_utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, area_sqft: float, bhk_count: int, age: int, 
                 locality_name: str, city: str, state: str, 
                 property_type: str, furnished_status: str, 
                 availability_status: str, metro_proximity_km: float, 
                 school_rating: int, future_infra_score: float):
        
        self.area_sqft = area_sqft
        self.bhk_count = bhk_count
        self.age = age
        self.locality_name = locality_name
        self.city = city
        self.state = state
        self.property_type = property_type
        self.furnished_status = furnished_status
        self.availability_status = availability_status
        # INVESTMENT FEATURES
        self.metro_proximity_km = metro_proximity_km
        self.school_rating = school_rating
        self.future_infra_score = future_infra_score

    def get_data_as_data_frame(self):
        try:
            # IMPORTANT: Keys must match the exact CSV column names for the preprocessor to work
            custom_data_input_dict = {
                "Size_in_SqFt": [self.area_sqft],
                "BHK": [self.bhk_count],
                "Age_of_Property": [self.age],
                "Locality": [self.locality_name],
                "City": [self.city],
                "State": [self.state],
                "Property_Type": [self.property_type],
                "Furnished_Status": [self.furnished_status],
                "Availability_Status": [self.availability_status],
                "metro_proximity_km": [self.metro_proximity_km],
                "school_rating": [self.school_rating],
                "future_infra_score": [self.future_infra_score]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)