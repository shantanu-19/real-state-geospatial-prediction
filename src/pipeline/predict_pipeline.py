import sys
import os
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
                 availability_status: str): # ADDED THIS
        self.area_sqft = area_sqft
        self.bhk_count = bhk_count
        self.age = age
        self.locality_name = locality_name
        self.city = city
        self.state = state
        self.property_type = property_type
        self.furnished_status = furnished_status
        self.availability_status = availability_status # ADDED THIS

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "area_sqft": [self.area_sqft],
                "bhk_count": [self.bhk_count],
                "age": [self.age],
                "locality_name": [self.locality_name],
                "city": [self.city],
                "state": [self.state],
                "property_type": [self.property_type],
                "furnished_status": [self.furnished_status],
                "availability_status": [self.availability_status], # ADDED THIS
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)