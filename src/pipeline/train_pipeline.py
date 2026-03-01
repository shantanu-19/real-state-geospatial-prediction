import sys
import os
import shutil

# Root path fix
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.utils.exception import CustomException

class TrainPipeline:
    def run_pipeline(self):
        try:
            # Clean artifacts folder first
            if os.path.exists("artifacts"):
                shutil.rmtree("artifacts")
            
            ingestion = DataIngestion()
            train_path, test_path = ingestion.initiate_data_ingestion()

            transformation = DataTransformation()
            train_arr, test_arr, _ = transformation.initiate_data_transformation(train_path, test_path)

            trainer = ModelTrainer()
            r2 = trainer.initiate_model_trainer(train_arr, test_arr)
            print(f"✅ Success! Training Complete. R2 Score: {r2}")

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    TrainPipeline().run_pipeline()