import os
import sys
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from src.utils.exception import CustomException
from src.utils.main_utils import save_object

class ModelTrainer:
    def initiate_model_trainer(self, train_array, test_array):
        try:
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], train_array[:, -1],
                test_array[:, :-1], test_array[:, -1]
            )

            # Deep Learning configuration for XGBoost
            model = XGBRegressor(
                n_estimators=1000,
                learning_rate=0.05,
                max_depth=8,
                subsample=0.8,
                colsample_bytree=0.8,
                n_jobs=-1
            )

            print("Model is learning property patterns...")
            model.fit(X_train, y_train)
            
            predicted = model.predict(X_test)
            score = r2_score(y_test, predicted)

            save_object(file_path=os.path.join("artifacts", "model.pkl"), obj=model)
            return score
        except Exception as e:
            raise CustomException(e, sys)