import os
import sys
import pickle
from src.utils.exception import CustomException
from src.utils.logger import logging

def save_object(file_path, obj):
    """Saves a python object (like a model or preprocessor) to a pickle file."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
        logging.info(f"Object saved successfully at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    """Loads a pickle file back into a python object."""
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)