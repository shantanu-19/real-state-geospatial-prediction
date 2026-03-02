import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.utils.exception import CustomException
from src.utils.logger import logging

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting Data Ingestion from MySQL")
        try:
            # Connect to MySQL
            engine = create_engine("mysql+mysqlconnector://root:Tanu**123@localhost/real_estate")
            
            # UPDATED QUERY: Pulling the 12 columns with the correct case-sensitive names
            query = """
            SELECT 
                Price_in_Lakhs, Size_in_SqFt, BHK, Age_of_Property, 
                Locality, City, State, Property_Type, 
                Furnished_Status, Availability_Status,
                metro_proximity_km, school_rating, future_infra_score
            FROM property_listings
            """
            df = pd.read_sql(query, engine)
            
            logging.info("Successfully read 12-column dataset from MySQL")

            # Create artifacts directory
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Save Raw Data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Train Test Split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            # Save Train and Test CSVs
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion complete. Names now match Transformation script.")
            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()