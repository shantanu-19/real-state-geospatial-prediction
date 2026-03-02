import sys
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from src.utils.exception import CustomException
from src.utils.main_utils import save_object

class DataTransformation:
    def get_transformer_object(self):
        try:
            # Matches the 12-column structure (9 original + 3 investment features)
            num_columns = [
                "Size_in_SqFt", 
                "BHK", 
                "Age_of_Property",
                "metro_proximity_km", 
                "school_rating", 
                "future_infra_score"
            ]
            
            cat_columns = [
                "Locality", 
                "City", 
                "State", 
                "Property_Type", 
                "Furnished_Status", 
                "Availability_Status"
            ]

            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ("target_encoder", TargetEncoder()), # Essential for high-cardinality localities
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("scaler", StandardScaler())
            ])

            return ColumnTransformer([
                ("num_pipeline", num_pipeline, num_columns),
                ("cat_pipeline", cat_pipeline, cat_columns)
            ])
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessing_obj = self.get_transformer_object()
            
            # Target column name must match your enhanced CSV
            target_col = "Price_in_Lakhs"

            X_train = train_df.drop(columns=[target_col], axis=1)
            y_train = train_df[target_col]
            X_test = test_df.drop(columns=[target_col], axis=1)
            y_test = test_df[target_col]

            # Fit and Transform
            # Note: TargetEncoder requires 'y_train' to map categories to price means
            X_train_arr = preprocessing_obj.fit_transform(X_train, y_train)
            X_test_arr = preprocessing_obj.transform(X_test)

            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]

            save_object(
                file_path=os.path.join('artifacts', "preprocessor.pkl"),
                obj=preprocessing_obj
            )
            
            return train_arr, test_arr, os.path.join('artifacts', "preprocessor.pkl")
            
        except Exception as e:
            raise CustomException(e, sys)