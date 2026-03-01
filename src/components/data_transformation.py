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
            # Defining columns for the 10-feature model
            num_columns = ["area_sqft", "bhk_count", "age"]
            cat_columns = [
                "locality_name", "city", "state", 
                "property_type", "furnished_status", "availability_status"
            ]

            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ("target_encoder", TargetEncoder()), # Secret to high R2
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
            target_col = "price_total"

            X_train = train_df.drop(columns=[target_col], axis=1)
            y_train = train_df[target_col]
            X_test = test_df.drop(columns=[target_col], axis=1)
            y_test = test_df[target_col]

            # Fit and Transform (TargetEncoder needs 'y' for fit)
            X_train_arr = preprocessing_obj.fit_transform(X_train, y_train)
            X_test_arr = preprocessing_obj.transform(X_test)

            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]

            save_object(file_path=os.path.join('artifacts', "preprocessor.pkl"), obj=preprocessing_obj)
            return train_arr, test_arr, "artifacts/preprocessor.pkl"
            
        except Exception as e:
            raise CustomException(e, sys)